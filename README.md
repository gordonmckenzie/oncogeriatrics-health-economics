### Oncogeriatrics health economic simulation

#### Introduction

This repository accompanies a scientific paper currently under peer-review. McKenzie *et al*., undertook a synthetic model-based health economic evaluation of geriatric assessment prior to cancer treatment. A model developed using the Python programming language has been packaged to share with the research community.

#### Description

This Python model has been packaged using [Poetry](https://python-poetry.org/) and can be used as follows. If you have Poetry already installed or wish to use for this project, follow the steps below: - 

#### Installation with Poetry

First, clone the repository into a suitable folder on your machine, following the instructions [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

Second, initialise the poetry shell by executing the following command in your terminal: -

`poetry shell`

Thirdly, install the dependencies: -

`poetry install`

#### Installation without Poetry

You can of course install and run this model without Poetry, provided the following dependencies are considered: -

- python = ">= 3.7.3, < 3.11"
- numpy = "^1.21.2"
- PyYAML = "^5.4.1"
- tabulate = "^0.8.9"
- pandas = "^1.3.3"
- scipy = "^1.7.1"

#### Running

For convenience a Makefile has been created to enable easing running of the model once installed. To run execute the following terminal command: -

`make run`

Without using poetry, execute: -

`python model.py`

#### Model modification 

We encourage other researchers to reuse this model and have therefore made it easy to adjust basic parameters with little coding knowledge. For more advanced modification, Python programming experience is required, but this model can be used as a foundation.

To adjust basic assumptions of the model, open the file `assumptions.yaml`. This is a [YAML Ain't Markup Language (YAML)](https://yaml.org/) file and is human and machine readable.

##### Basic

| Parameters  | Description | Default       |
| ----------- | ----------- | ------------- |
| `simulations`      | The number of Monte Carlo simulations to undertake       | 5000
| `progress`   | Whether to show a progress bar or not in the terminal output       | True
| `treatment-distributions` | The distributions of different treatments in the following order: - <ul><li>other care</li><li>chemotherapy only</li><li>surgery only</li><li>radiotherapy only</li><li>radiotherapy only</li><li>chemotherapy and radiotherapy</li><li>surgery and chemotherapy</li><li>surgery and radiotherapy</li><li>surgery, radiotherapy and chemotherapy</li></ul> | `[0.335175413, 0.083228036, 0.209740598, 0.147376245, 0.049030028, 0.074862494, 0.072866805, 0.027720381]` derived from [NHS Cancer Data](https://www.cancerdata.nhs.uk/treatments), assumed for a 77-year-old patient |

##### Implementation

| Parameters  | Description | Default       |
| ----------- | ----------- | ------------- |
| `tablet-based-assessments` | Patients have the option of completing a geriatric assessment on a tablet device | False
| `face-to-face-assessments-nurse` | Patients are being seen face-to-face by a nurse | True
| `face-to-face-assessments-consultant` | Patients are being seen face-to-face by a Consultant (Attending) Physician | True
| `face-to-face-assessments-registrar` | Patients are being seen face-to-face by a Specialist Registrar (Resident) Physician | False
| `telephone-assessments` | A nurse is undertaking telephone assessments | False
| `remote-assessments-where-possible` | Where possible, remote patient-reported assessements are being undertaken | False
| `ga-changing-management-at-mdt-level` | The results from the geriatric assessment are changing management at the cancer multi-disciplinary team (tumour board) level | True
| `only-undergoing-chemotherapy` | Patients are only undergoing geriatric assessment before chemotherapy | False
| `only-undergoing-surgery` | Patients are only undergoing geriatric assessment before surgery | False

##### Clinical effectiveness of Geriatric Assessment

| Parameters  | Description | Default       |
| ----------- | ----------- | ------------- |
| `reduced-los-effect` | Geriatric assessment reduces length of stay (relative risk) | 1 |
| `reduced-chemotherapy-toxicity-effect` | Geriatric assessment reduces chemotherapy toxicity | True |
| `reduced-er-visits-effect` | Geriatric assessment reduces emergency department (room) visits (relative risk) | 1 |
| `reduced-itu-admissions-effect` | Geriatric assessment reduces intenstive therapy unit admissions (relative risk) | 1 |
| `reduced-surgical-complications-effect` | Geriatric assessment reduces post-operative complications | True |
| `reduced-post-surgical-readmissions-effect` |  Geriatric assessment reduces post-operative complications  (relative risk) | 1 |

##### Surgical parameters

| Parameters  | Description | Default       |
| ----------- | ----------- | ------------- |
| `bed-days-alpha` | The $\alpha$ parameter of a Gamma distribution for postoperative bed days | 2.14 |
| `bed-days-beta` | The $\beta$ parameter of a Gamma distribution for postoperative bed days | 3.04 |
| `requiring-itu` | The percentage requiring Intensive Care Unit admission postoperatively | 0.097 |
| `readmissions-alpha` | The $\alpha$ parameter of a Beta distribution for postoperative readmissions | 3.6 |
| `readmissions-beta` | The $\beta$ parameter of a Beta distribution for postoperative readmissions | 31.5 |

##### General parameters

| Parameters  | Description | Default       |
| ----------- | ----------- | ------------- |
| `er-visits-alpha` | The $\alpha$ parameter of a Beta distribution for emergency department (room) visits | 0.78  |
| `er-visits-beta` | The $\beta$ parameter of a Gamma distribution for emergency department (room) visits | 6.31 |
| `initial-qaly-alpha` | The $\alpha$ parameter of a Beta distribution for the initial quality-adjusted life year before treatment | 37.79 |
| `initial-qaly-beta` | The $\beta$ parameter of a Beta distribution for the initial quality-adjusted life year before treatment | 13.93 |
| `10-year-survival-probabilities` | The 10-year survival probabilties of 77-year-old adults with cancer -/+ postoperative complications | `[[ 0.967711, 0.612698, 0.52797, 0.473091, 0.438158, 0.413269, 0.3908, 0.370723, 0.354533, 0.343723, 0.339788 ], [ 0.967711, 0.571380518, 0.464723943, 0.395256173, 0.356781234, 0.328020278, 0.301236405, 0.277092946, 0.259023145, 0.243354875, 0.230547149 ]]` |
| `nice-recommended-yearly-discount` | The National Institute of Health and Care Excellence recommended yearly discount in quality-adjusted life years | 0.035 |
| `chemotherapy-qaly-decrement-alpha` | The $\alpha$ parameter of a Beta distribution for the decrement in quality-adjusted life years during and following chemotherapy (lasts on year) | 77.05 |
| `chemotherapy-qaly-decrement-beta` | The $\beta$ parameter of a Beta distribution for the decrement in quality-adjusted life years during and following chemotherapy (lasts on year) | 163.73 | 

#### Unit costs

The unit costs can be found in the `utilisation_costs.yaml` file. These are again editable to account for cost changes and international differences. 

##### Pretreatment costs

| Parameters  | Description | Default (£)   |
| ----------- | ----------- | ------------- |
| `ga-using-tablet-technology` | The cost per patient to use technology to assist geriatric assessment | 2 |
| `ga-using-tablet-staff` | The cost of staff per patient to use technology to assist geriatric assessment  | 68.78 |
| `ga-using-consultant` | The cost of a Consultant (attending) Physician to undertake a 30-minute component of geriatric assessment | 141.18 |
| `ga-using-registrar` | The cost of a Specialist Registrar (Resident) Physician to undertake a 30-minute component of geriatric assessment | 169.23 |
| `ga-using-nurse-f2f` | The cost of a Band 6 nurse to undertake a 60-minute component of geriatric assessment | 117.91 |
| `ga-using-telephone-nurse-led` | The cost of a Band 6 nurse to undertake a 30-minute geriatric assessment over the phone | 117.91 |
| `dietician` | The cost of a dietician to undertake a 30-minute assessment | 58.96 |
| `social-worker` | The cost of a social worker to undertake a 30-minute assessment | 32.51 |
| `occupational-therapy` | The cost of a occupational therapist to undertake a 30-minute assessment | 60.23 |
| `physiotherapist` | The cost of a physiotherapist to undertake a 30-minute assessment | 60.23 |
| `falls-clinic` | The cost of a falls clinic attendance | 747.07 |
| `outpatient-physician` | The cost of a 30-minute appointment with an outpatient Consultant (Attending) Physician | 141.18 |
| `cbt-course` | The cost of a course of Cognitive Behavioural Therapy per patient | 1053.40 |

##### Posttreatment costs

| Parameters  | Description | Default (£)   |
| ----------- | ----------- | ------------- |
| `excess-bed-day` | The cost of an excess bed day following surgery | 366.01 |
| `hdu-or-itu-admission` | The cost of a High Dependency Unit or Intensive Care Unit admission | 2160.21 |
| `chemotherapy-toxicity-short-stay` | The cost of a short (1 day) admission for chemotherapy toxicity | 614.75 |
| `chemotherapy-toxicity-long-stay` | The cost of a long (5 days +) admission for chemotherapy toxicity | 3437.29 |
| `er-visits` | The cost of an emergency department (room) visit | 169.92 |
| `surgical-readmission` | The cost of a readmission following surgery | 3522.70 |

##### Unmet needs

Unmet need is difficult to model economically, but the differences in the identification of unmet needs between standard care and introducing geriatric assessment are shown below. These are contained within the `parameters.yaml` file. The key values to modify are the mean, upper and lower limits of each parameters for the relevant arm (standard care *versus* standard care and geriatric assessment).

#### License

This code is MIT licensed (see `license.md`) and we encourage other researchers to reuse and advance this model for the benefit of oncogeriatric research. We would be most grateful if you could kindly cite our final article when published if you have used this model in your research. 

