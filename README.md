# **Explainable AI Tool for Label-Free Non-Normal RBC Morphology Classification**
## Or simply "Cell Classifier" for now
---

# Explainable RBC Morphology Analysis Tool

## Table of Contents

1. [Project Overview](#project-overview)
2. [Motivation & Impact](#motivation--impact)
3. [Scope & Objectives](#scope--objectives)
4. [Biological Background](#biological-background)

   * [Normal RBC Structure & Function](#normal-rbc-structure--function)
   * [Non-Normal RBC Shapes & Clinical Significance](#non-normal-rbc-shapes--clinical-significance)
5. [Experimental Design & Data Generation](#experimental-design--data-generation)

   * [Osmolarity Conditions](#osmolarity-conditions)
   * [Salt Modulators & Age Groups](#salt-modulators--age-groups)
   * [Data Acquisition Workflow](#data-acquisition-workflow)
6. [System Architecture & Modules](#system-architecture--modules)

   1. [Data Ingestion](#1-data-ingestion)
   2. [Pre-Processing & Enhancement](#2-pre-processing--enhancement)
   3. [Segmentation Engine](#3-segmentation-engine)
   4. [Feature Extraction](#4-feature-extraction)
   5. [Morphology Classification](#5-morphology-classification)
   6. [Explainability Layer](#6-explainability-layer)
   7. [GUI & Annotation Interface](#7-gui--annotation-interface)
   8. [Export & Reporting](#8-export--reporting)
7. [Data & Metadata Specification](#data--metadata-specification)

   * [Image Formats & Naming Conventions](#image-formats--naming-conventions)
   * [JSON Schema for Cell Records](#json-schema-for-cell-records)
8. [User Workflows](#user-workflows)

   * [Pathologist Annotation Flow](#pathologist-annotation-flow)
   * [Batch Processing Flow](#batch-processing-flow)
   * [Time-Series Tracking Flow](#time-series-tracking-flow)
9. [Development Roadmap & Milestones](#development-roadmap--milestones)
10. [Technology Stack](#technology-stack)
11. [Team Roles & Responsibilities](#team-roles--responsibilities)
12. [Future Extensions](#future-extensions)
13. [References](#references)

---

## Project Overview

We are developing a **user-friendly**, **explainable** software suite for the automated segmentation, classification, and analysis of red blood cell (RBC) morphologies in label-free (brightfield) microscopy images.  Pathologists will be able to:

* Upload TIFF stacks or single-frame images
* Inspect and correct individual cell crops and labels via an interactive GUI
* Export per-cell metadata (shape, features, classification probabilities, explanations) in JSON/CSV
* Aggregate statistics at the sample or time-series level

Ultimately, the tool powers an **automated, AI-driven** pipeline to accelerate both research and clinical workflows around RBC shape analysis.

---

## Motivation & Impact

* **Clinical Diagnostics:** Aberrant RBC shapes (e.g., spherocytes, elliptocytes) are hallmarks of hemolytic anemias, membrane disorders, and storage lesions.
* **Research Utility:** Controlled in vitro modulation of RBC shape expands our understanding of membrane biomechanics, drug effects, and ion-channel function.
* **Data Generation:** Generating high-quality, annotated datasets of RBC morphologies under varying osmotic and ionic conditions fills a gap in publicly available resources.
* **Explainable AI:** Embedding interpretability (via feature‐based rules, SHAP/LIME) ensures pathologist trust and facilitates regulatory acceptance.

---

## Scope & Objectives

1. **High-throughput Segmentation:** Automatically detect and crop every RBC in a frame.
2. **Rich Feature Extraction:** Compute size (area, equivalent diameter), shape (solidity, aspect ratio), and intensity/textural descriptors per cell.
3. **Morphology Classification:** Assign each crop to one of 9–13 clinically relevant shape classes, with probabilities.
4. **Explainability:** Provide per-cell rationales (feature contributions) for each label.
5. **Annotation GUI:** Build a web-based front end to review/correct segmentation and classification before AI training.
6. **Time-Series Tracking:** (Future) Link cell appearances across frames to study dynamic shape changes.
7. **Export & Integration:** JSON/CSV output plus cropped image sets for downstream AI/analytics.

---

## Biological Background

### Normal RBC Structure & Function

* **Diameter & Shape:** \~7.5–8.2 µm biconcave disc, maximizing surface-to-volume ratio.
* **Membrane Composition:** Lipid bilayer coupled to spectrin cytoskeleton (2D network), facilitating deformability.
* **Physiological Role:** Transport O₂/CO₂; negotiate narrow capillaries (2–3 µm).
* **Lifespan:** \~120 days; aging leads to gradual shape deviations.

### Non-Normal RBC Shapes & Clinical Significance

| Morphology          | Description & Etiology                                                      |
| ------------------- | --------------------------------------------------------------------------- |
| **Microspherocyte** | Spherical RBCs; associated with hereditary spherocytosis, immune hemolysis. |
| **Elliptocyte**     | Oval/elliptical RBCs; seen in hereditary elliptocytosis.                    |
| **Target Cell**     | Central staining spot; thalassemia, liver disease.                          |
| **Acanthocyte**     | Spiky projections; abetalipoproteinemia, liver dysfunction.                 |
| **Echinocyte**      | Burr cells; artifact, uremia, pyruvate kinase deficiency.                   |
| **Stomatocyte**     | Mouth-shaped slit; ethanol, hereditary stomatocytosis.                      |

Referenced from Gallagher & Jarolim, 2008 (“Bessis’s Red Cell Shapes”).

---

## Experimental Design & Data Generation

### Osmolarity Conditions

* **Hypotonic (260–285 mOsm/kg)**
* **Normotonic (286–300 mOsm/kg)**
* **Hypertonic (301–315 mOsm/kg)**

(Prepared and verified using an osmometer.)

### Salt Modulators & Age Groups

* **Salts:** NaCl, KCl, CaCl₂, MgCl₂, Choline Chloride (as proxies for ionic influences)
* **Age Groups:** Young (0–30 days), Mid (31–60 days), Old (61–120 days)
* **Total Conditions:** 3 osmolarities × 5 salts × 3 age groups = **45 unique solutions**

### Data Acquisition Workflow

1. **Sample Preparation:** Incubate washed RBCs in each condition for X minutes at 37 °C.
2. **Imaging:** Acquire 10–20 brightfield TIFF stacks per condition, each stack 100–200 frames.
3. **Storage:** Organize data directory as:

   ```
   /data/
     /osmotic_<hypo|norm|hyper>/
       /salt_<name>/
         /age_<young|mid|old>/
           sample01.tiff, sample02.tiff, …
   ```
4. **Initial QC:** Discard out-of-focus or over-saturated stacks.

---

## System Architecture & Modules

### 1. Data Ingestion

* **Formats Supported:** Single-image TIFF, multi-frame TIFF stacks, PNG/JPEG (for tests)
* **Metadata Capture:** Filename, frame index, acquisition timestamp

### 2. Pre-Processing & Enhancement

* **Flat-field Correction:** Normalize illumination using sliding-window background estimation.
* **Contrast Enhancement:** CLAHE (Contrast-Limited Adaptive Histogram Equalization) for weak-contrast cells.
* **Noise Reduction:** Median or bilateral filtering to suppress speckle.

### 3. Segmentation Engine

1. **Classical Pipeline (baseline):**

   * Grayscale → Otsu/Adaptive threshold → morphological closing → remove\_small\_objects
   * Label connected components → compute `regionprops`.
2. **Deep Learning Pipeline (future):**

   * Lightweight U-Net trained on manually annotated RBC masks (128×128 patches)
   * Output: binary mask per frame → post-processing as above.

### 4. Feature Extraction

* **Shape Descriptors:**

  * Area, perimeter, equivalent diameter
  * Solidity, eccentricity, aspect ratio
* **Intensity/Textural Features:**

  * Mean, standard deviation of pixel intensity
  * Haralick texture metrics (contrast, correlation)
* **Advanced:**

  * Fourier shape descriptors
  * Zernike moments (for high-order morphology detail)

### 5. Morphology Classification

* **Rule-Based Prototype:**

  * Thresholds on aspect ratio, solidity, convexity to assign shape classes.
* **Machine-Learning Model:**

  * Random Forest or XGBoost on extracted features → class probabilities.
* **Training Data:**

  * Initially, 1,000–2,000 manually reviewed crops across all 45 conditions.

### 6. Explainability Layer

* **Feature Contribution:**

  * SHAP values per feature for each prediction.
* **Visual Rationale:**

  * Display top-3 features driving the classification in the GUI (e.g., “High solidity favored spherocyte”).

### 7. GUI & Annotation Interface

* **Web-Based (React + Flask/Django):**

  * Drag-and-drop TIFF stacks or select folders.
  * Real-time overlay of segmentation bboxes & labels.
  * Click cell → view crop + feature table + SHAP explanation.
  * Edit label or adjust bbox, save corrections back to JSON.

### 8. Export & Reporting

* **Per-Cell JSON Record:**

  * `{ id, source_image, frame_idx, bbox, centroid, features, class_label, class_prob, explanation }`
* **Batch CSV/Excel:** Summary statistics per morphology class per sample.
* **Cropped Images:** Organized into `/crops/<sample>/<frame>/cell_<ID>.png`

---

## Data & Metadata Specification

### Image Formats & Naming Conventions

```
<data_root>/
  sample_<condition>_<replicate>.tiff
  sample_<condition>_<replicate>.json
```

* **TIFF Stack:** multi-page, metadata tags preserved.
* **JSON:** same basename, contains list of crop records.

### JSON Schema for Cell Records

```json
{
  "cells": [
    {
      "cell_id": "sample01_f0001_c023",
      "frame_index": 1,
      "bbox": [x_min, y_min, width, height],
      "centroid": [x, y],
      "features": {
        "area": 42.7,
        "perimeter": 28.3,
        "solidity": 0.92,
        "eccentricity": 0.18,
        "mean_intensity": 127.8,
        "...": "..."
      },
      "predicted_class": "spherocyte",
      "class_probability": 0.87,
      "explanation": {
        "solidity": +0.23,
        "aspect_ratio": -0.15,
        "mean_intensity": +0.05
      }
    }
    // … more cells
  ]
}
```

---

## User Workflows

### Pathologist Annotation Flow

1. **Load Sample:** Pathologist selects one or more TIFF stacks.
2. **Review Overlays:** GUI displays detected bboxes + labels.
3. **Inspect & Correct:**

   * Click a bbox → pop-up shows crop + feature table + SHAP bar chart.
   * Adjust label or delete false detection.
4. **Save Annotations:** Updates JSON; corrections stored for retraining.

### Batch Processing Flow

1. **CLI/Config:** Define input folder, output folder, parameters (thresholds, min\_area).
2. **Run Segmentation:**

   ```bash
   python segment_and_extract.py --input data/ --output results/ --config cfg.yaml
   ```
3. **Generate JSON + Crops:** All cells processed, results saved.

### Time-Series Tracking Flow (Future)

1. **Inter-Frame Matching:** Nearest-centroid or Hungarian algorithm to link cells.
2. **Trajectory JSON:** Append `track_id` to each cell record.
3. **Visualization:** Plot morphology class over time per track in GUI.

---

## Development Roadmap & Milestones

| Phase                                                   | Goals & Deliverables                                                     | Timeline      |
| ------------------------------------------------------- | ------------------------------------------------------------------------ | ------------- |
| **Phase 1:** Setup & Baseline (Days 1–5)                | Env setup, sample loading, classical segmentation prototype, JSON export | End of Week 1 |
| **Phase 2:** GUI MVP & Annotation (Weeks 2–3)           | Basic React UI, overlay display, manual annotation save/load             | Mid Week 3    |
| **Phase 3:** ML & Explainability (Weeks 4–6)            | Feature extraction module, RF classifier, integrate SHAP explanations    | End Week 6    |
| **Phase 4:** Dataset Expansion & Validation (Weeks 7–9) | Run 45 conditions, pathologist annotation, retrain models                | End Week 9    |
| **Phase 5:** Time-Series & Advanced (Weeks 10–12)       | Tracking module, dynamic visualization, performance benchmarking         | End Week 12   |

---

## Technology Stack

* **Core Language:** Python 3.9+
* **Imaging & ML:**

  * `numpy`, `scikit-image`, `tifffile`, `opencv-python`
  * `scikit-learn`, `xgboost`, `shap`
  * (Future) `torch`, `segmentation_models_pytorch`
* **Web Frontend:** React + Tailwind CSS + shadcn/ui
* **Backend API:** Flask or Django REST Framework
* **Data Storage:** Local filesystem (with eventual S3 support)
* **Version Control & CI:** GitHub + GitHub Actions + pytest

---

## Team Roles & Responsibilities

| Role                      | Responsibilities                                               |
| ------------------------- | -------------------------------------------------------------- |
| **Project Lead (You)**    | Overall design, segmentation prototype, feature module         |
| **Pre-Clinician Scholar** | Experimental design, data generation, biological guidance      |
| **Web UI Developer**      | GUI design, annotation interface, frontend–backend integration |
| **ML Engineer**           | Classifier development, explainability integration             |
| **QA/Pathologist**        | Annotation validation, user acceptance testing                 |

---

## Future Extensions

* **3D Imaging Support:** Confocal stacks → volumetric segmentation.
* **Integration with LIMS:** Link cell data to patient/sample metadata.
* **Cloud Deployment:** Scalable processing via AWS/GCP containers.
* **Mobile Interface:** Rapid on-site slide QC on tablets.

---

## References

1. Gallagher PG, Jarolim P. *Red Cell Membrane and Cytoskeleton*. Wiley, 1999.
2. Föller M., et al. “Ion Channel Regulation in Erythrocytes,” *Blood Cells, Molecules & Diseases*, 2020.
3. Haralick RM, Shanmugam K, Dinstein I. “Textural Features for Image Classification,” *IEEE TPAMI*, 1973.

---

*End of document.*
