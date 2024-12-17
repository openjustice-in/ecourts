# ecourts [![Coverage Status](https://coveralls.io/repos/github/captn3m0/ecourts/badge.svg?branch=main)](https://coveralls.io/github/captn3m0/ecourts?branch=main) [![PyPI - Latest Version](https://img.shields.io/pypi/v/ecourts)](https://pypi.org/project/ecourts/) [![GitHub Tag](https://img.shields.io/github/v/tag/captn3m0/ecourts?filter=v*)](https://github.com/captn3m0/ecourts/releases/latest) [![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/captn3m0/ecourts/test.yml?branch=main)](https://github.com/captn3m0/ecourts/actions/workflows/test.yml) [![docs](https://img.shields.io/badge/docs-Guide-9b59b6)](https://openjustice-in.github.io/ecourts/) [![docs](https://img.shields.io/badge/docs-API_Reference-9b59b6)](https://openjustice-in.github.io/ecourts/src/) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13324986.svg)](https://doi.org/10.5281/zenodo.13324986)

This is a information retrieval toolkit to fetch case information from the
ECourts Service. This is primarily meant for journalists, and law
researchers who need bulk access to the ECourts website to get orders,
judgements, or lists of cases that match their criteria.

The final goal is to cover all services under the `ecourts.gov.in` domain, but it currently
supports a few services covered at https://hcservices.ecourts.gov.in/ecourtindiaHC/.

It covers all the High Courts and their various benches.

Type of Query | Supported | Inputs
--------------|-----------|-------
Search for cases by Case Number   | 🚧WIP | Case Type, Case Number, Year
Search for cases by FIR Number | 🚧WIP | Police Station, FIR Number†, Year†, Case Status (Pending/Disposed/Both)†
Search for cases by Party Name | 🔜Planned | Petitioner/Respondent Name, Year†, Case Status (Pending/Disposed/Both)†
Search for cases by Advocate Name | 🚫No
Search for cases by Filing Number | 🚧WIP | Filing Number, Year
Search for cases by Act | ✅Yes | Act Type, Status
Search for cases by Case Type | 🚧WIP | Case Type, Year†, Pending/Disposed
Search for Case Orders/Judgement by Case Number | 🚧WIP | Case Type, Case Number, Year
Search for Case Orders/Judgement by Filling Number | 🚧WIP | Filing Number, Year
Search for Case Orders/Judgement by Judge Wise | 🚫No |
Search for Case Orders/Judgement by Party Name | 🔜Planned | Petitioner/Respondent Name, Year
Search for Case Orders/Judgement by Order Date | ✅Yes | Date
Get Cause List | ✅Yes | Date|

**† - Optional**

## Case Types

Each of the individual courts use their own numbering system for various case-types. So the same type of case might have different ID depending on the court. This can even vary between various benches of the same High Court. For example, HCB (Habeas Corpus Petition) is numbered the following different ways across various courts (not exhaustive):

Court |ID
------|----
Madras High Court - Principal Bench| 22
Madras High Court - Madurai Bench | 164
High Court of Jammu and Kashmir - Jammu Wing|17
High Court of Jammu and Kashmir - Srinagar Wing|171

As such, before doing any kind of work that relies on case type (such as fetching case details, or orders by case type) - you must get the relevant case type idenfiers. You can run:

`ecourts get-case-type --state-code SC [--court-code CC]` to
get the case type identifiers for a particular court. If the
`state-code/court-code` identifiers are not provided, the case types will
be fetched for all known courts. A list of all known courts is available
at [courts.csv](courts.csv) published as part of the source code.

## Act Types

Similar to Case Types, Act idenfiers are different between courts. You can use

`ecourts get-act-type --state-code SC [--court-code CC]` 
to get the act type identifiers for a particular court.

## Types

The primary two classes that most users will deal with are Court, and ECourt. A court is one of the high court benches covered at https://hcservices.ecourts.gov.in/ecourtindiaHC/,
and an ECourt is the primary class that deals with the website.

Other entities involved are more legal in nature:

- [Case](https://openjustice-in.github.io/ecourts/src/entities/case.html#src.entities.case.Case)
- [CaseType](https://openjustice-in.github.io/ecourts/src/entities/case_type.html)
- [ActType](https://openjustice-in.github.io/ecourts/src/entities/act_type.html)
- [FIR](https://openjustice-in.github.io/ecourts/src/entities/fir.html)
- [Hearing](https://openjustice-in.github.io/ecourts/src/entities/hearing.html)
- [Objection](https://openjustice-in.github.io/ecourts/src/entities/objection.html)
- [Order](https://openjustice-in.github.io/ecourts/src/entities/order.html) - An order or judgement in a case.
- [Party](https://openjustice-in.github.io/ecourts/src/entities/party.html) - Either a petitioner or a responded to a case.
- [Court](https://openjustice-in.github.io/ecourts/src/entities/court.html)
- [ECourt](https://openjustice-in.github.io/ecourts/src/ecourt.html) APIs are also documented.

## Documentation

- Canonical link for the project is <https://openjustice-in.github.io/ecourts/>.
- General guidance is available via `ecourts --help` or `ecourts cmd --help`.
- Python documentation is available at [openjustice-in.github.io/ecourts/src](https://openjustice-in.github.io/ecourts/src/).
- Coverage reports are published at [Coveralls](https://coveralls.io/github/captn3m0/ecourts).

## Guiding Principles

- Make it easy to fetch case information.
- Store information in accessible formats, for easy retrieval and querying.
- Use standard identifiers, such as ISO-3166 for state codes.
- Be nice to the ecourts website. Retry failed requests, but do not hammer the site.
  In case of 5xx errors, wait for a while before retrying.

## Citation [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13324986.svg)](https://doi.org/10.5281/zenodo.13324986)

If you use this for any research purposes, please use the following
citation information. 

> DOI: https://doi.org/10.5281/zenodo.13324986

You can check various citation formats on the [Zenodo Website](https://zenodo.org/records/13324986)
or on GitHub by clicking "Cite this repository". Since this is a dynamic software - it 
depends on the ecourts website, please cite the Zenodo ID `13324986` as it will always
point to the latest version of the software.

## LICENSE

Licensed under `GPL3-or-later`. If you run this code, you are responsible
for the legal implications of the same. The tool is intentionally
single-threaded, and does not offer any parallelism. This is to avoid
overloading the ecourts website servers, which are already
quite slow. Please note sections 15-16 of the LICENSE, which are summarized here:

```
There is no warranty for the program, to the extent permitted by
applicable law. In no event unless required by applicable law or agreed to in
writing will any copyright holder, or any other party who modifies and/or
conveys the program as permitted above, be liable to you for damages,
including any general, special, incidental or consequential damages arising
out of the use or inability to use the program.
```

As part of GPL3 obligations:

>You may copy, distribute and modify the software as long as you track
 changes/dates in source files. Any modifications to this code must also be
 made available under the GPL along with build & install instructions.
