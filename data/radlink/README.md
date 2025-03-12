# RadLink Dataset Structure

## Overview
RadLink数据集包含了放射学报告的标注数据，数据从RadGraph数据集中的训练集和开发集中抽取。  

### train
train 里有Length of data: 425
Length of all_unique_entities_dict: 1250
Number of entities: 12388 1250个 entity。

### train + dev
500 reports 
train + dev 里有 1353个 entity。

一共是**1353**个entity。[not_normalized.csv](not_normalized.csv)

预览 [not_normalized.csv](not_normalized.csv):

| name | ui | normalized_name | semanticTypes | definition |
| --- | --- | --- | --- | --- |
| Lungs | | | | |
| clear | | | | |
| Normal | | | | |
| ... | ... | ... | ... | ... |

1353个 entity 。

## simple output after umls search

[simple_output.csv](simple_output.csv) 

| name | ui | normalized_name |
| --- | --- | --- |
| Lungs | C0024109 | Lungs |
| clear | C2963144 | clear |
| Normal | C0205307 | Normal |
| ... | ... | ... |

1250个entity。  
number of not normalized rows: 362  
number of normalized rows: 888

TODO: 需要检查，数量不对。重新跑一下 1353 的数据，

## output.csv **after gpt processing**

目前[output.csv](output.csv) is **after gpt processing** but before human review. 

| name | ui | normalized_name |
| --- | --- | --- |
| Lungs | C0024109 | Lungs |
| clear | C2963144 | clear |
| Normal | C0205307 | Normal |
| ... | ... | ... |

1250个entity。


## reviews.xlsx
[reviews.xlsx](reviewed.xlsx) 1250个entity。

| name | ui | normalized_name | semanticTypes | definition | report | Radiology Expert verify | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Lungs | C0024109 | Lungs | Body Part, Organ, or Organ Component | Lobular organ with a parenchyma consisting of air-filled alveoli which communicate with the tracheobronchial tree. Examples: There are only two instances, right lung and left lung. | FINAL REPORT EXAMINATION : CHEST ( PORTABLE AP ) INDICATION : ___ year old woman with SAH / / Fever workup Fever workup IMPRESSION : Compared to chest radiographs ___ . Patient has been extubated . Lungs are clear . Normal cardiomediastinal and hilar silhouettes and pleural surfaces . | Yes | i would write it like that: lobular organ with a parenchyma consisting of… |
| ... | ... | ... | ... | ... | ... | ... | ... |

1250个entity。

## reviews.csv
| name | ui | normalized_name |
| --- | --- | --- |
| Lungs | C0024109 | Lungs |
| clear | C2963144 | clear |
| Normal | C0205307 | Normal |
| cardiomediastinal | | |
| ... | ... | ... |

1250个entity。
