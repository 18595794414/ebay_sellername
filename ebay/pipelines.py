# -*- coding: utf-8 -*-


from .items import EbayItemGood
from .items import EbayItemShop



class SavePipeline(object):
    item1 = []
    item2 = []

    def process_item(self, item, spider):

        if isinstance(item, EbayItemShop):

            data = (item['seller_name'], item['followers_num'], item['country'], item['positive_feedback_percer'],item['Feedback_score'], item['Item_s_described_score'], item['Communication_score'],item['Shipping_time_score'], item['Shipping_charges_score'], item['seller_text'],item['Positive_feedback'], item['Neutral_feedback'], item['Negative_feedback'], item['views'],item['Reviews'], item['goods_num'], item['Member_since'], item['shop_url'])

            self.item1.append(data)

            if len(self.item1) == 10:
                for i in self.item1:
                    with open(r'D:/Spider_Demo/ebay/shopinfo.txt', 'a', encoding='utf-8') as f:
                        f.write(str(i) + ',' + '\n')
                self.item1 = []


        elif isinstance(item, EbayItemGood):

            data = (item['good_id'], item['good_name'], item['price_dollar'], item['price_RMB'], item['project_location'],item['brand'], item['seller_name'], item['sales_count'], item['cat_1'], item['cat_2'], item['cat_3'], item['cat_4'],item['cat_5'], item['cat_6'])

            self.item2.append(data)

            if len(self.item2) == 20:
                for i in self.item2:
                    with open(r'D:/Spider_Demo/ebay/goodsinfo.txt', 'a', encoding='utf-8') as f:
                        f.write(str(i) + ',' +'\n')
                self.item2 = []

        return item

