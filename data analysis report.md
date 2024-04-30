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
    3. 台北房源的價格區間

## 1.台北房源的區域分布
* 使用語法
```
SELECT `host_neighbourhood`,COUNT(`host_neighbourhood`) AS 'location' FROM `taipei`
WHERE `host_neighbourhood` IS NOT NULL
GROUP BY `host_neighbourhood` ORDER BY `location` DESC;
```
使用COUNT對host_neighbourhood欄位計數，得到各個區域房源數量。並用python畫出區域數量圓餅圖  

![image](https://hackmd.io/_uploads/r1ATbQCZC.png)
* 如圖可知，最多房源的行政區為萬華區，占了台北市房源約1/4，其次則為大安區19%、中正區13.7%，這三區的房源占比達到了整個台北市的5%左右。
* 為何萬華的房源那麼多?我認為是因為這裡坐落著台灣最有名的商業區-西門町

## 2.台北房源類型的比例，並和其他大城市做比較