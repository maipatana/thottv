# thottv

This module is intended to be used for Overall Thermal Transfer Value calculation, 

โมดูลนี้เขียนขึ้นมาเพื่อใช้สำหรับการคนำวณ OTTV/RTTV/WBC ตาม[ประกาศกระทรวงพลังงาน](https://maipatana.me/static/%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%81%E0%B8%B2%E0%B8%A8%E0%B8%81%E0%B8%A3%E0%B8%B0%E0%B8%97%E0%B8%A3%E0%B8%A7%E0%B8%87%E0%B8%9E%E0%B8%A5%E0%B8%B1%E0%B8%87%E0%B8%87%E0%B8%B2%E0%B8%99.pdf)

## วิธีการใช้งาน
ขั้นตอนการทำงาน
1. สร้าง construction ซึ่งก็คือ section ของเปลือกอาคาร  ```con(ชื่อ)```
2. ใส่ material เข้าไปใน construction ซึ่งก็คือ layer ต่างๆ ```.add_mat(ชื่อ, ความหนา, k, r, cp)```

3. สร้าง wall ```wall(ชื่อ, orientation, tilt)```
4. ใส่ construction เข้าไปใน wall ```.add_con(con(), พื้นที่, ค่าการดูลืนรังสีอาทิตย์)``` โดยค่าการดูดกลืนระบุตามสีภายนอก 0.3 ขาวสะท้อน 0.9 เข้ม
    หนึ่งผนังด้านเดียวกันสามารถมีหลาย construction ได้
5. ระบุด้านของผนัง ```.set_ori(องศา)``` โดย 0 คือทิศใต้ 90 คือทิศตะวันตก 180 คือทิศเหนือ และ 270 คือทิศตะวันออก

6. สร้าง space ```space(ชื่อ, พื้นที่, ประเภท)```
7. ใส่ wall เข้าไปใน space ```.add_wall(wall())```

8. ค่า OTTV ที่ได้คือ ```.get_ottv()```

## Update 26-Dec-2017
ปัจจุบัน Module นี้ยังไม่เสร็จสิ้น ยังไม่เหมาะสมที่จะนำไปใช้งาน
สิ่งที่จะทำต่อไป:
- เพิ่มกระจก
- ให้รู้จัก airgap และ insulation
- คำนวณ RTTV
- ใส่ข้อมูลใน ```wall.TDED_LIST``` และ ```materials_list()```
