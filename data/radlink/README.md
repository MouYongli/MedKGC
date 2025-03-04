# RadLink Dataset Structure

## Overview
RadLink数据集包含了放射学报告的标注数据，数据从RadGraph数据集中的训练集和开发集中抽取。
一共是**1353**个entity。[not_normalized.csv](not_normalized.csv)

预览 [not_normalized.csv](not_normalized.csv):

| name | ui | normalized_name | semanticTypes | definition |
| --- | --- | --- | --- | --- |
| Lungs | | | | |
| clear | | | | |
| Normal | | | | |
| ... | ... | ... | ... | ... |


## simple output after umls search

[simple_output.csv](simple_output.csv) 1250个entity。  
number of not normalized rows: 362  
number of normalized rows: 888

| name | ui | normalized_name |
| --- | --- | --- |
| Lungs | C0024109 | Lungs |
| clear | C2963144 | clear |
| Normal | C0205307 | Normal |
| ... | ... | ... |



## output.csv **after gpt processing**

目前[output.csv](output.csv) is **after gpt processing** but before human review. 1250个entity。

| name | ui | normalized_name |
| --- | --- | --- |
| Lungs | C0024109 | Lungs |
| clear | C2963144 | clear |
| Normal | C0205307 | Normal |
| ... | ... | ... |


## reviews
[reviews.xlsx](reviewed.xlsx) 

| name | ui | normalized_name | semanticTypes | definition | report | Radiology Expert verify | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Lungs | C0024109 | Lungs | Body Part, Organ, or Organ Component | Lobular organ with a parenchyma consisting of air-filled alveoli which communicate with the tracheobronchial tree. Examples: There are only two instances, right lung and left lung. | FINAL REPORT EXAMINATION : CHEST ( PORTABLE AP ) INDICATION : ___ year old woman with SAH / / Fever workup Fever workup IMPRESSION : Compared to chest radiographs ___ . Patient has been extubated . Lungs are clear . Normal cardiomediastinal and hilar silhouettes and pleural surfaces . | Yes | i would write it like that: lobular organ with a parenchyma consisting of… |
| ... | ... | ... | ... | ... | ... | ... | ... |
