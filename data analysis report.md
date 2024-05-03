# airbnb在台北房源現況分析
## 緒論
* 這是一個資料分析的專案練習，由於我十分喜愛旅遊，因此旅遊住宿相關的方向作為主題進行分析  

## airbnb介紹
* airbnb全稱為air bed and breakfast，是一間提供短期租屋的網站，和一般的的訂房網站不同，airbnb的房源大多來自於私人民宅或套房，主打貼近當地的生活體驗。  
* 截至2022年，airbnb的全球有效房源已有600萬間，遍布超過220個國家，入住人次更是超過10億人次  
## 使用程式語言/工具
* 使用mySQL進行資料分析，並使用python的matplotlib.pyplot函示庫繪圖

## 分析題目
* 我打算利用透過這個報告回答以下幾個問題:
    1. 台北房源的區域分布
    2. 台北房源類型的比例，並和其他大城市做比較
    3. 台北房源的價格區間及比較

## 1.台北房源的區域分布
* 使用語法
```sql!
SELECT `host_neighbourhood`,COUNT(`host_neighbourhood`) AS 'location' FROM `taipei`
WHERE `host_neighbourhood` IS NOT NULL
GROUP BY `host_neighbourhood` ORDER BY `location` DESC;
```
使用COUNT對host_neighbourhood欄位計數，得到各個區域房源數量。並用python畫出區域數量圓餅圖  

![image](https://hackmd.io/_uploads/r1ATbQCZC.png)
* 如圖可知，最多房源的行政區為萬華區，占了台北市房源約1/4，其次則為大安區19%、中正區13.7%，這三區的房源占比達到了整個台北市的5%左右。
* 為何萬華的房源那麼多?我認為是因為這裡坐落著台灣最有名的商業區-西門町

## 2.台北房源類型的比例，並和其他大城市做比較
* 房源類型分為4種，分別為entire home/apt(整棟房子/公寓)、private room(私人房間)、hotel(旅館)、shared room(共享房間)
```sql
SELECT t.`room_type`,COUNT(t.`room_type`) AS 'taipei',
r.`rome` AS 'rome',san.`san_francisco` AS 'san_francisco'
FROM `taipei` t

INNER JOIN (SELECT `room_type`,COUNT(`room_type`) AS 'rome'
FROM `rome` GROUP by `room_type`) r
ON r.`room_type`=t.`room_type`

INNER JOIN (SELECT `room_type`,COUNT(`room_type`) AS 'san_francisco'
FROM `san francisco` GROUP by `room_type`) san
ON san.`room_type`=t.`room_type` GROUP BY t.`room_type`;")
```
* 使用INNER JOIN內部連接，將舊金山和羅馬的資料連接後一起顯示，輸出表格如下


| room_type | Taipei | Rome | San Francisco |
| -------- | -------- | -------- | -------- |
| Entire home | 3159 | 20743 | 4923 |
| Private room | 1256 | 7873 | 3304 |
| Hotel | 118 | 596 | 62 |
| Shared room | 227 | 145 | 72 |

* 接著使用python畫出房源類型長條圖(y軸為百分比)  
![taipei](https://hackmd.io/_uploads/ByroB5kMR.png)
![rome](https://hackmd.io/_uploads/rJsiS5kG0.png)
![san francisco](https://hackmd.io/_uploads/ryajHcyfA.png)
* 透過圖表可以得知以下資訊  
    1. 性質接近民宿的entire home和private room超過了90%，而旅館占比<2%。和airbnb的成立初衷相似  
    2. 共享房間在台北的占比(4.8%)較羅馬(0.5%)和舊金山(0.9%)高，和我預想的相反。也許台灣對於共享房間的接受度並不低  

## 3.台北房源的價格區間及比較
* 近幾年，國內旅館一直給人價格高昂的印象，但私人經營的民宿是否也有這個狀況呢?  
* 首先，我統計了每種房源類型的平均價格，並且為了篩選掉一些可能沒在經營的住宿，限制房源的評論數量多於5筆才會納入平均價格的計算中。  
* 此外，以東京、雪梨、曼谷的資料作為對照組  
```sql!
SELECT t.`room_type`,ROUND(AVG(REPLACE(REPLACE(t.`price`,'$',''),',','')),2) AS 'taipei',j.`tokyo` AS 'tokyo',s.`sydney` AS 'sydney',b.`bangkok` AS 'bangkok' FROM `taipei` t

INNER JOIN (SELECT `room_type`,ROUND(AVG(REPLACE(REPLACE(`price`,'$',''),',','')),2) AS 'tokyo' FROM `tokyo` WHERE `number_of_reviews`>5 GROUP BY `room_type`) j
ON j.`room_type`=t.`room_type`

INNER JOIN (SELECT `room_type`,ROUND(AVG(REPLACE(REPLACE(`price`,'$',''),',','')),2) AS 'sydney' FROM `sydney` WHERE `number_of_reviews`>5 GROUP BY `room_type`) s
ON s.`room_type`=t.`room_type`

INNER JOIN (SELECT `room_type`,ROUND(AVG(REPLACE(REPLACE(`price`,'$',''),',','')),2) AS 'bangkok' FROM `bangkok` WHERE `number_of_reviews`>5 GROUP BY `room_type`) b

ON b.`room_type`=t.`room_type`
WHERE `number_of_reviews`>5 GROUP BY `room_type`;
```
![avg_price](https://hackmd.io/_uploads/Hk83PQWGA.png)
* 在所有類型中，台北的價格都只高於曼谷，低於東京和雪梨。  
* 在hotel的類型中，台北的價格十分接近東京，而entire home和private room則有一定差距。  
* 由此可以推測，台灣的旅館價格確實偏貴，但私人經營的民宿則沒有此情況。  
* 單純透過airbnb的資料進行分析推測，因此上面的結果僅供參考。  
* 旅館的價格還會受到位置(是否為風景區)、時間(平日/假日)的影響，如果要做更進一步的研究，上面兩點也需要考慮。