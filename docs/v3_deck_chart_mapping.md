# MDS-MDSDATA - Charts & Code used in the deck (MDS - FUU)

Folder packaging for the case competition organizers.

It contains ONLY the charts that actually appear in the deck `MDS - FUU (15).pdf`
(31 pages) together with the Python script that generates each chart.

- Total charts used: 37
- Source data: `cleaned_dataset.xlsx` (sheet `Dataset_Clean`, n=2.600)

> **Supplementary (NOT in the original PDF):** `slide 5 - Consumer Profile/s5_scale_opportunity_north.png`
> (+ `chart_scale_opportunity_north.py`) — added to present the North region as the largest
> scale opportunity (870 aware-but-not-using = 51% of national conversion pool; +71% headroom to Mekong's 37%).

## Mapping: deck page -> chart -> code

| PDF page | Section | Chart file | Code |
|---|---|---|---|
| 5 | slide 3 - Segmentation Matrix | `s3_segmatrix.png` | `charts_slide3_matrix.py` |
| 7 | slide 5 - Consumer Profile | `s5_cozy_reach_region.png` | `charts_slide5.py` |
| 7 | slide 6 - Brand Funnel | `s6_funnel.png` | `charts_slide7.py` |
| 8 | slide 6 - Brand Funnel | `s6_conversion.png` | `charts_slide7.py` |
| 8 | slide 6 - Brand Funnel | `s6_funnel_compare.png` | `charts_slide7.py` |
| 9 | slide 7 - Root Cause Barriers | `s7_barriers_cluster.png` | `charts_slide7.py` |
| 10 | slide 8 - Image Void | `s8_attr_heatmap.png` | `charts_slide8.py` |
| 10 | slide 8 - Image Void | `s8_dumbbell.png` | `charts_slide8.py` |
| 11 | slide 9 - Touchpoint | `s9_funnel_concept.png` | `charts_slide9.py` |
| 11 | slide 9 - Touchpoint | `s9_tom.png` | `charts_slide9.py` |
| 11 | slide 9 - Touchpoint | `s9_touchpoint.png` | `charts_slide9.py` |
| 12 | slide 10 - Availability | `s10_barrier.png` | `charts_slide10.py` |
| 12 | slide 10 - Availability | `s10_instore.png` | `charts_slide10.py` |
| 12 | slide 10 - Availability | `s10_repeat.png` | `charts_slide10.py` |
| 12 | slide 10 - Availability | `s10_trialhabit.png` | `charts_slide10.py` |
| 14 | slide 5 - Consumer Profile | `s5_cozy_p4w_age_yoy.png` | `charts_slide5.py` |
| 14 | slide 5 - Consumer Profile | `s5_gender_30plus.png` | `charts_slide5.py` |
| 14 | slide 5 - Consumer Profile | `s5_gender_growth_30plus.png` | `charts_slide5.py` |
| 14 | slide 5 - Consumer Profile | `s5_income.png` | `charts_slide5.py` |
| 14 | slide 5 - Consumer Profile | `s5_intensity_age.png` | `charts_slide5.py` |
| 16 | slide 8b - Persona | `s8b_persona.png` | `charts_slide8b.py` |
| 17 | slide 5 - Consumer Profile | `s5_cozy_olong_region.png` | `charts_slide5.py` |
| 17 | slide 5 - Consumer Profile | `s5_income_region.png` | `charts_slide5.py` |
| 17 | slide 5 - Consumer Profile | `s5_region_donut.png` | `charts_slide5.py` |
| 18 | misc | `slide_POPvsSocial_only_green_16x9.png` | `(no source script found)` |
| 19 | SKU Hero Products | `sku_herovai.png` | `charts_sku_hero.py` |
| 19 | slide 11 - SKU Hero | `s11_bumo.png` | `charts_slide11.py` |
| 20 | SKU Hero Products | `sku_dao.png` | `charts_sku_hero.py` |
| 20 | slide 16 - Value Chain & Pillars | `s_flavor_opportunity.png` | `charts_slide16.py` |
| 22 | slide 13 - Positioning | `s13_house.png` | `charts_slide13.py` |
| 24 | slide 15 - Roadmap | `s15_roadmap.png` | `charts_slide15.py` |
| 29 | slide 16 - Value Chain & Pillars | `s16_budget_v2.png` | `charts_slide16.py` |
| 29 | slide 16 - Value Chain & Pillars | `s16_sizing.png` | `charts_slide16.py` |
| 31 | slide 16 - Value Chain & Pillars | `s16_enabler_research.png` | `charts_slide16.py` |
| 31 | slide 16 - Value Chain & Pillars | `s16_pillar1_product.png` | `charts_slide16.py` |
| 31 | slide 16 - Value Chain & Pillars | `s16_pillar2_distribution.png` | `charts_slide16.py` |
| 31 | slide 16 - Value Chain & Pillars | `s16_pillar3_activation.png` | `charts_slide16.py` |

## Notes
- Each `slide N - ...` subfolder holds the used chart PNG(s) plus its generating script `charts_slideN*.py`.
- A generating script may also produce other charts that were NOT used in the final deck; only the used PNGs were moved here.
- `misc/slide_POPvsSocial_only_green_16x9.png` was exported/renamed manually; no matching source script was found in the repo.