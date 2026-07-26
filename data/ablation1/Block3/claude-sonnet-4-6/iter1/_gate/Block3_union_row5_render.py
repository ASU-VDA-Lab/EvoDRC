import pya

layout = pya.Layout()
layout.dbu = 0.00025

cell_VIA_VIA45 = layout.create_cell("VIA_VIA45")
cell_VIA_VIA34 = layout.create_cell("VIA_VIA34")
cell_VIA_VIA23 = layout.create_cell("VIA_VIA23")
cell_VIA_VIA12 = layout.create_cell("VIA_VIA12")
cell_VIA_via1_2_2322_18_1_64_36_36 = layout.create_cell("VIA_via1_2_2322_18_1_64_36_36")
cell_VIA_VIA23_1_3_36_36 = layout.create_cell("VIA_VIA23_1_3_36_36")
cell_VIA_VIA34_1_2_58_52 = layout.create_cell("VIA_VIA34_1_2_58_52")
cell_VIA_VIA45_1_2_58_58 = layout.create_cell("VIA_VIA45_1_2_58_58")
cell_BUFx3_ASAP7_75t_R = layout.create_cell("BUFx3_ASAP7_75t_R")
cell_BUFx12f_ASAP7_75t_R = layout.create_cell("BUFx12f_ASAP7_75t_R")
cell_BUFx6f_ASAP7_75t_R = layout.create_cell("BUFx6f_ASAP7_75t_R")
cell_BUFx2_ASAP7_75t_R = layout.create_cell("BUFx2_ASAP7_75t_R")
cell_FAx1_ASAP7_75t_R = layout.create_cell("FAx1_ASAP7_75t_R")
cell_INVx2_ASAP7_75t_R = layout.create_cell("INVx2_ASAP7_75t_R")
cell_INVx3_ASAP7_75t_R = layout.create_cell("INVx3_ASAP7_75t_R")
cell_TAPCELL_ASAP7_75t_R = layout.create_cell("TAPCELL_ASAP7_75t_R")
cell_DECAPx2_ASAP7_75t_R = layout.create_cell("DECAPx2_ASAP7_75t_R")
cell_FILLER_ASAP7_75t_R = layout.create_cell("FILLER_ASAP7_75t_R")
cell_FILLERxp5_ASAP7_75t_R = layout.create_cell("FILLERxp5_ASAP7_75t_R")
cell_Block3 = layout.create_cell("Block3")

cell_Block3.name = "Block3"

p0 = pya.Polygon([pya.Point(-48, -92), pya.Point(-48, 92), pya.Point(48, 92), pya.Point(48, -92)])
# polygon_id: p0
cell_VIA_VIA45.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p0)
p1 = pya.Polygon([pya.Point(-92, -48), pya.Point(-92, 48), pya.Point(92, 48), pya.Point(92, -48)])
# polygon_id: p1
cell_VIA_VIA45.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1)
p2 = pya.Polygon([pya.Point(-48, -48), pya.Point(-48, 48), pya.Point(48, 48), pya.Point(48, -48)])
# polygon_id: p2
cell_VIA_VIA45.shapes(layout.layer(pya.LayerInfo(45, 0))).insert(p2)
p3 = pya.Polygon([pya.Point(-80, -48), pya.Point(-80, 48), pya.Point(80, 48), pya.Point(80, -48)])
# polygon_id: p3
cell_VIA_VIA34.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p3)
p4 = pya.Polygon([pya.Point(-36, -68), pya.Point(-36, 68), pya.Point(36, 68), pya.Point(36, -68)])
# polygon_id: p4
cell_VIA_VIA34.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p4)
p5 = pya.Polygon([pya.Point(-36, -48), pya.Point(-36, 48), pya.Point(36, 48), pya.Point(36, -48)])
# polygon_id: p5
cell_VIA_VIA34.shapes(layout.layer(pya.LayerInfo(35, 0))).insert(p5)
p6 = pya.Polygon([pya.Point(-36, -56), pya.Point(-36, 56), pya.Point(36, 56), pya.Point(36, -56)])
# polygon_id: p6
cell_VIA_VIA23.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p6)
p7 = pya.Polygon([pya.Point(-56, -36), pya.Point(-56, 36), pya.Point(56, 36), pya.Point(56, -36)])
# polygon_id: p7
cell_VIA_VIA23.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p7)
p8 = pya.Polygon([pya.Point(-36, -36), pya.Point(-36, 36), pya.Point(36, 36), pya.Point(36, -36)])
# polygon_id: p8
cell_VIA_VIA23.shapes(layout.layer(pya.LayerInfo(25, 0))).insert(p8)
p9 = pya.Polygon([pya.Point(-56, -36), pya.Point(-56, 36), pya.Point(56, 36), pya.Point(56, -36)])
# polygon_id: p9
cell_VIA_VIA12.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p9)
p10 = pya.Polygon([pya.Point(-36, -44), pya.Point(-36, 44), pya.Point(36, 44), pya.Point(36, -44)])
# polygon_id: p10
cell_VIA_VIA12.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p10)
p11 = pya.Polygon([pya.Point(-36, -36), pya.Point(-36, 36), pya.Point(36, 36), pya.Point(36, -36)])
# polygon_id: p11
cell_VIA_VIA12.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p11)
p12 = pya.Polygon([pya.Point(-4580, -36), pya.Point(-4580, 36), pya.Point(4580, 36), pya.Point(4580, -36)])
# polygon_id: p12
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p12)
p13 = pya.Polygon([pya.Point(-4572, -36), pya.Point(-4572, 36), pya.Point(4572, 36), pya.Point(4572, -36)])
# polygon_id: p13
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p13)
p14 = pya.Polygon([pya.Point(-4572, -36), pya.Point(-4572, 36), pya.Point(-4500, 36), pya.Point(-4500, -36)])
# polygon_id: p14
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p14)
p15 = pya.Polygon([pya.Point(-4428, -36), pya.Point(-4428, 36), pya.Point(-4356, 36), pya.Point(-4356, -36)])
# polygon_id: p15
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p15)
p16 = pya.Polygon([pya.Point(-4284, -36), pya.Point(-4284, 36), pya.Point(-4212, 36), pya.Point(-4212, -36)])
# polygon_id: p16
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p16)
p17 = pya.Polygon([pya.Point(-4140, -36), pya.Point(-4140, 36), pya.Point(-4068, 36), pya.Point(-4068, -36)])
# polygon_id: p17
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p17)
p18 = pya.Polygon([pya.Point(-3996, -36), pya.Point(-3996, 36), pya.Point(-3924, 36), pya.Point(-3924, -36)])
# polygon_id: p18
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p18)
p19 = pya.Polygon([pya.Point(-3852, -36), pya.Point(-3852, 36), pya.Point(-3780, 36), pya.Point(-3780, -36)])
# polygon_id: p19
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p19)
p20 = pya.Polygon([pya.Point(-3708, -36), pya.Point(-3708, 36), pya.Point(-3636, 36), pya.Point(-3636, -36)])
# polygon_id: p20
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p20)
p21 = pya.Polygon([pya.Point(-3564, -36), pya.Point(-3564, 36), pya.Point(-3492, 36), pya.Point(-3492, -36)])
# polygon_id: p21
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p21)
p22 = pya.Polygon([pya.Point(-3420, -36), pya.Point(-3420, 36), pya.Point(-3348, 36), pya.Point(-3348, -36)])
# polygon_id: p22
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p22)
p23 = pya.Polygon([pya.Point(-3276, -36), pya.Point(-3276, 36), pya.Point(-3204, 36), pya.Point(-3204, -36)])
# polygon_id: p23
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p23)
p24 = pya.Polygon([pya.Point(-3132, -36), pya.Point(-3132, 36), pya.Point(-3060, 36), pya.Point(-3060, -36)])
# polygon_id: p24
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p24)
p25 = pya.Polygon([pya.Point(-2988, -36), pya.Point(-2988, 36), pya.Point(-2916, 36), pya.Point(-2916, -36)])
# polygon_id: p25
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p25)
p26 = pya.Polygon([pya.Point(-2844, -36), pya.Point(-2844, 36), pya.Point(-2772, 36), pya.Point(-2772, -36)])
# polygon_id: p26
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p26)
p27 = pya.Polygon([pya.Point(-2700, -36), pya.Point(-2700, 36), pya.Point(-2628, 36), pya.Point(-2628, -36)])
# polygon_id: p27
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p27)
p28 = pya.Polygon([pya.Point(-2556, -36), pya.Point(-2556, 36), pya.Point(-2484, 36), pya.Point(-2484, -36)])
# polygon_id: p28
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p28)
p29 = pya.Polygon([pya.Point(-2412, -36), pya.Point(-2412, 36), pya.Point(-2340, 36), pya.Point(-2340, -36)])
# polygon_id: p29
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p29)
p30 = pya.Polygon([pya.Point(-2268, -36), pya.Point(-2268, 36), pya.Point(-2196, 36), pya.Point(-2196, -36)])
# polygon_id: p30
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p30)
p31 = pya.Polygon([pya.Point(-2124, -36), pya.Point(-2124, 36), pya.Point(-2052, 36), pya.Point(-2052, -36)])
# polygon_id: p31
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p31)
p32 = pya.Polygon([pya.Point(-1980, -36), pya.Point(-1980, 36), pya.Point(-1908, 36), pya.Point(-1908, -36)])
# polygon_id: p32
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p32)
p33 = pya.Polygon([pya.Point(-1836, -36), pya.Point(-1836, 36), pya.Point(-1764, 36), pya.Point(-1764, -36)])
# polygon_id: p33
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p33)
p34 = pya.Polygon([pya.Point(-1692, -36), pya.Point(-1692, 36), pya.Point(-1620, 36), pya.Point(-1620, -36)])
# polygon_id: p34
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p34)
p35 = pya.Polygon([pya.Point(-1548, -36), pya.Point(-1548, 36), pya.Point(-1476, 36), pya.Point(-1476, -36)])
# polygon_id: p35
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p35)
p36 = pya.Polygon([pya.Point(-1404, -36), pya.Point(-1404, 36), pya.Point(-1332, 36), pya.Point(-1332, -36)])
# polygon_id: p36
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p36)
p37 = pya.Polygon([pya.Point(-1260, -36), pya.Point(-1260, 36), pya.Point(-1188, 36), pya.Point(-1188, -36)])
# polygon_id: p37
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p37)
p38 = pya.Polygon([pya.Point(-1116, -36), pya.Point(-1116, 36), pya.Point(-1044, 36), pya.Point(-1044, -36)])
# polygon_id: p38
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p38)
p39 = pya.Polygon([pya.Point(-972, -36), pya.Point(-972, 36), pya.Point(-900, 36), pya.Point(-900, -36)])
# polygon_id: p39
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p39)
p40 = pya.Polygon([pya.Point(-828, -36), pya.Point(-828, 36), pya.Point(-756, 36), pya.Point(-756, -36)])
# polygon_id: p40
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p40)
p41 = pya.Polygon([pya.Point(-684, -36), pya.Point(-684, 36), pya.Point(-612, 36), pya.Point(-612, -36)])
# polygon_id: p41
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p41)
p42 = pya.Polygon([pya.Point(-540, -36), pya.Point(-540, 36), pya.Point(-468, 36), pya.Point(-468, -36)])
# polygon_id: p42
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p42)
p43 = pya.Polygon([pya.Point(-396, -36), pya.Point(-396, 36), pya.Point(-324, 36), pya.Point(-324, -36)])
# polygon_id: p43
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p43)
p44 = pya.Polygon([pya.Point(-252, -36), pya.Point(-252, 36), pya.Point(-180, 36), pya.Point(-180, -36)])
# polygon_id: p44
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p44)
p45 = pya.Polygon([pya.Point(-108, -36), pya.Point(-108, 36), pya.Point(-36, 36), pya.Point(-36, -36)])
# polygon_id: p45
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p45)
p46 = pya.Polygon([pya.Point(36, -36), pya.Point(36, 36), pya.Point(108, 36), pya.Point(108, -36)])
# polygon_id: p46
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p46)
p47 = pya.Polygon([pya.Point(180, -36), pya.Point(180, 36), pya.Point(252, 36), pya.Point(252, -36)])
# polygon_id: p47
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p47)
p48 = pya.Polygon([pya.Point(324, -36), pya.Point(324, 36), pya.Point(396, 36), pya.Point(396, -36)])
# polygon_id: p48
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p48)
p49 = pya.Polygon([pya.Point(468, -36), pya.Point(468, 36), pya.Point(540, 36), pya.Point(540, -36)])
# polygon_id: p49
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p49)
p50 = pya.Polygon([pya.Point(612, -36), pya.Point(612, 36), pya.Point(684, 36), pya.Point(684, -36)])
# polygon_id: p50
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p50)
p51 = pya.Polygon([pya.Point(756, -36), pya.Point(756, 36), pya.Point(828, 36), pya.Point(828, -36)])
# polygon_id: p51
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p51)
p52 = pya.Polygon([pya.Point(900, -36), pya.Point(900, 36), pya.Point(972, 36), pya.Point(972, -36)])
# polygon_id: p52
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p52)
p53 = pya.Polygon([pya.Point(1044, -36), pya.Point(1044, 36), pya.Point(1116, 36), pya.Point(1116, -36)])
# polygon_id: p53
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p53)
p54 = pya.Polygon([pya.Point(1188, -36), pya.Point(1188, 36), pya.Point(1260, 36), pya.Point(1260, -36)])
# polygon_id: p54
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p54)
p55 = pya.Polygon([pya.Point(1332, -36), pya.Point(1332, 36), pya.Point(1404, 36), pya.Point(1404, -36)])
# polygon_id: p55
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p55)
p56 = pya.Polygon([pya.Point(1476, -36), pya.Point(1476, 36), pya.Point(1548, 36), pya.Point(1548, -36)])
# polygon_id: p56
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p56)
p57 = pya.Polygon([pya.Point(1620, -36), pya.Point(1620, 36), pya.Point(1692, 36), pya.Point(1692, -36)])
# polygon_id: p57
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p57)
p58 = pya.Polygon([pya.Point(1764, -36), pya.Point(1764, 36), pya.Point(1836, 36), pya.Point(1836, -36)])
# polygon_id: p58
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p58)
p59 = pya.Polygon([pya.Point(1908, -36), pya.Point(1908, 36), pya.Point(1980, 36), pya.Point(1980, -36)])
# polygon_id: p59
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p59)
p60 = pya.Polygon([pya.Point(2052, -36), pya.Point(2052, 36), pya.Point(2124, 36), pya.Point(2124, -36)])
# polygon_id: p60
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p60)
p61 = pya.Polygon([pya.Point(2196, -36), pya.Point(2196, 36), pya.Point(2268, 36), pya.Point(2268, -36)])
# polygon_id: p61
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p61)
p62 = pya.Polygon([pya.Point(2340, -36), pya.Point(2340, 36), pya.Point(2412, 36), pya.Point(2412, -36)])
# polygon_id: p62
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p62)
p63 = pya.Polygon([pya.Point(2484, -36), pya.Point(2484, 36), pya.Point(2556, 36), pya.Point(2556, -36)])
# polygon_id: p63
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p63)
p64 = pya.Polygon([pya.Point(2628, -36), pya.Point(2628, 36), pya.Point(2700, 36), pya.Point(2700, -36)])
# polygon_id: p64
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p64)
p65 = pya.Polygon([pya.Point(2772, -36), pya.Point(2772, 36), pya.Point(2844, 36), pya.Point(2844, -36)])
# polygon_id: p65
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p65)
p66 = pya.Polygon([pya.Point(2916, -36), pya.Point(2916, 36), pya.Point(2988, 36), pya.Point(2988, -36)])
# polygon_id: p66
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p66)
p67 = pya.Polygon([pya.Point(3060, -36), pya.Point(3060, 36), pya.Point(3132, 36), pya.Point(3132, -36)])
# polygon_id: p67
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p67)
p68 = pya.Polygon([pya.Point(3204, -36), pya.Point(3204, 36), pya.Point(3276, 36), pya.Point(3276, -36)])
# polygon_id: p68
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p68)
p69 = pya.Polygon([pya.Point(3348, -36), pya.Point(3348, 36), pya.Point(3420, 36), pya.Point(3420, -36)])
# polygon_id: p69
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p69)
p70 = pya.Polygon([pya.Point(3492, -36), pya.Point(3492, 36), pya.Point(3564, 36), pya.Point(3564, -36)])
# polygon_id: p70
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p70)
p71 = pya.Polygon([pya.Point(3636, -36), pya.Point(3636, 36), pya.Point(3708, 36), pya.Point(3708, -36)])
# polygon_id: p71
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p71)
p72 = pya.Polygon([pya.Point(3780, -36), pya.Point(3780, 36), pya.Point(3852, 36), pya.Point(3852, -36)])
# polygon_id: p72
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p72)
p73 = pya.Polygon([pya.Point(3924, -36), pya.Point(3924, 36), pya.Point(3996, 36), pya.Point(3996, -36)])
# polygon_id: p73
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p73)
p74 = pya.Polygon([pya.Point(4068, -36), pya.Point(4068, 36), pya.Point(4140, 36), pya.Point(4140, -36)])
# polygon_id: p74
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p74)
p75 = pya.Polygon([pya.Point(4212, -36), pya.Point(4212, 36), pya.Point(4284, 36), pya.Point(4284, -36)])
# polygon_id: p75
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p75)
p76 = pya.Polygon([pya.Point(4356, -36), pya.Point(4356, 36), pya.Point(4428, 36), pya.Point(4428, -36)])
# polygon_id: p76
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p76)
p77 = pya.Polygon([pya.Point(4500, -36), pya.Point(4500, 36), pya.Point(4572, 36), pya.Point(4572, -36)])
# polygon_id: p77
cell_VIA_via1_2_2322_18_1_64_36_36.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p77)
p78 = pya.Polygon([pya.Point(-180, -56), pya.Point(-180, 56), pya.Point(180, 56), pya.Point(180, -56)])
# polygon_id: p78
cell_VIA_VIA23_1_3_36_36.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p78)
p79 = pya.Polygon([pya.Point(-200, -36), pya.Point(-200, 36), pya.Point(200, 36), pya.Point(200, -36)])
# polygon_id: p79
cell_VIA_VIA23_1_3_36_36.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p79)
p80 = pya.Polygon([pya.Point(108, -36), pya.Point(108, 36), pya.Point(180, 36), pya.Point(180, -36)])
# polygon_id: p80
cell_VIA_VIA23_1_3_36_36.shapes(layout.layer(pya.LayerInfo(25, 0))).insert(p80)
p81 = pya.Polygon([pya.Point(-36, -36), pya.Point(-36, 36), pya.Point(36, 36), pya.Point(36, -36)])
# polygon_id: p81
cell_VIA_VIA23_1_3_36_36.shapes(layout.layer(pya.LayerInfo(25, 0))).insert(p81)
p82 = pya.Polygon([pya.Point(-180, -36), pya.Point(-180, 36), pya.Point(-108, 36), pya.Point(-108, -36)])
# polygon_id: p82
cell_VIA_VIA23_1_3_36_36.shapes(layout.layer(pya.LayerInfo(25, 0))).insert(p82)
p83 = pya.Polygon([pya.Point(-184, -48), pya.Point(-184, 48), pya.Point(184, 48), pya.Point(184, -48)])
# polygon_id: p83
cell_VIA_VIA34_1_2_58_52.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p83)
p84 = pya.Polygon([pya.Point(-160, -68), pya.Point(-160, 68), pya.Point(160, 68), pya.Point(160, -68)])
# polygon_id: p84
cell_VIA_VIA34_1_2_58_52.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p84)
p85 = pya.Polygon([pya.Point(68, -48), pya.Point(68, 48), pya.Point(140, 48), pya.Point(140, -48)])
# polygon_id: p85
cell_VIA_VIA34_1_2_58_52.shapes(layout.layer(pya.LayerInfo(35, 0))).insert(p85)
p86 = pya.Polygon([pya.Point(-140, -48), pya.Point(-140, 48), pya.Point(-68, 48), pya.Point(-68, -48)])
# polygon_id: p86
cell_VIA_VIA34_1_2_58_52.shapes(layout.layer(pya.LayerInfo(35, 0))).insert(p86)
p87 = pya.Polygon([pya.Point(-240, -92), pya.Point(-240, 92), pya.Point(240, 92), pya.Point(240, -92)])
# polygon_id: p87
cell_VIA_VIA45_1_2_58_58.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p87)
p88 = pya.Polygon([pya.Point(-208, -48), pya.Point(-208, 48), pya.Point(208, 48), pya.Point(208, -48)])
# polygon_id: p88
cell_VIA_VIA45_1_2_58_58.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p88)
p89 = pya.Polygon([pya.Point(68, -48), pya.Point(68, 48), pya.Point(164, 48), pya.Point(164, -48)])
# polygon_id: p89
cell_VIA_VIA45_1_2_58_58.shapes(layout.layer(pya.LayerInfo(45, 0))).insert(p89)
p90 = pya.Polygon([pya.Point(-164, -48), pya.Point(-164, 48), pya.Point(-68, 48), pya.Point(-68, -48)])
# polygon_id: p90
cell_VIA_VIA45_1_2_58_58.shapes(layout.layer(pya.LayerInfo(45, 0))).insert(p90)
p91 = pya.Polygon([pya.Point(580, 108), pya.Point(580, 180), pya.Point(1152, 180), pya.Point(1152, 900), pya.Point(580, 900), pya.Point(580, 972), pya.Point(1224, 972), pya.Point(1224, 108)])
# polygon_id: p91
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p91)
p92 = pya.Polygon([pya.Point(160, 108), pya.Point(160, 180), pya.Point(408, 180), pya.Point(408, 900), pya.Point(160, 900), pya.Point(160, 972), pya.Point(480, 972), pya.Point(480, 576), pya.Point(1040, 576), pya.Point(1040, 504), pya.Point(480, 504), pya.Point(480, 108)])
# polygon_id: p92
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p92)
p93 = pya.Polygon([pya.Point(72, 252), pya.Point(72, 828), pya.Point(220, 828), pya.Point(220, 756), pya.Point(144, 756), pya.Point(144, 576), pya.Point(292, 576), pya.Point(292, 504), pya.Point(144, 504), pya.Point(144, 324), pya.Point(220, 324), pya.Point(220, 252)])
# polygon_id: p93
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p93)
p94 = pya.Polygon([pya.Point(0, -36), pya.Point(0, 36), pya.Point(1296, 36), pya.Point(1296, -36)])
# polygon_id: p94
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p94)
p95 = pya.Polygon([pya.Point(0, 1044), pya.Point(0, 1116), pya.Point(1296, 1116), pya.Point(1296, 1044)])
# polygon_id: p95
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p95)
p96 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(1296, 1080), pya.Point(1296, 540)])
# polygon_id: p96
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(13, 0))).insert(p96)
p97 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(1296, 1080), pya.Point(1296, 540)])
# polygon_id: p97
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(1, 0))).insert(p97)
p98 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 1080), pya.Point(1296, 1080), pya.Point(1296, 0)])
# polygon_id: p98
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(100, 0))).insert(p98)
p99 = pya.Polygon([pya.Point(1032, 108), pya.Point(1032, 432), pya.Point(1128, 432), pya.Point(1128, 108)])
# polygon_id: p99
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p99)
p100 = pya.Polygon([pya.Point(1032, 648), pya.Point(1032, 972), pya.Point(1128, 972), pya.Point(1128, 648)])
# polygon_id: p100
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p100)
p101 = pya.Polygon([pya.Point(816, 0), pya.Point(816, 432), pya.Point(912, 432), pya.Point(912, 0)])
# polygon_id: p101
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p101)
p102 = pya.Polygon([pya.Point(816, 648), pya.Point(816, 1080), pya.Point(912, 1080), pya.Point(912, 648)])
# polygon_id: p102
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p102)
p103 = pya.Polygon([pya.Point(600, 108), pya.Point(600, 432), pya.Point(696, 432), pya.Point(696, 108)])
# polygon_id: p103
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p103)
p104 = pya.Polygon([pya.Point(600, 648), pya.Point(600, 972), pya.Point(696, 972), pya.Point(696, 648)])
# polygon_id: p104
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p104)
p105 = pya.Polygon([pya.Point(384, 0), pya.Point(384, 432), pya.Point(480, 432), pya.Point(480, 0)])
# polygon_id: p105
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p105)
p106 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 1080), pya.Point(480, 1080), pya.Point(480, 648)])
# polygon_id: p106
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p106)
p107 = pya.Polygon([pya.Point(168, 108), pya.Point(168, 432), pya.Point(264, 432), pya.Point(264, 108)])
# polygon_id: p107
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p107)
p108 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 972), pya.Point(264, 972), pya.Point(264, 648)])
# polygon_id: p108
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p108)
p109 = pya.Polygon([pya.Point(1032, 108), pya.Point(1032, 432), pya.Point(1128, 432), pya.Point(1128, 108)])
# polygon_id: p109
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p109)
p110 = pya.Polygon([pya.Point(1032, 648), pya.Point(1032, 972), pya.Point(1128, 972), pya.Point(1128, 648)])
# polygon_id: p110
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p110)
p111 = pya.Polygon([pya.Point(816, 108), pya.Point(816, 432), pya.Point(912, 432), pya.Point(912, 108)])
# polygon_id: p111
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p111)
p112 = pya.Polygon([pya.Point(816, 648), pya.Point(816, 972), pya.Point(912, 972), pya.Point(912, 648)])
# polygon_id: p112
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p112)
p113 = pya.Polygon([pya.Point(600, 108), pya.Point(600, 432), pya.Point(696, 432), pya.Point(696, 108)])
# polygon_id: p113
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p113)
p114 = pya.Polygon([pya.Point(600, 648), pya.Point(600, 972), pya.Point(696, 972), pya.Point(696, 648)])
# polygon_id: p114
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p114)
p115 = pya.Polygon([pya.Point(384, 108), pya.Point(384, 432), pya.Point(480, 432), pya.Point(480, 108)])
# polygon_id: p115
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p115)
p116 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 972), pya.Point(480, 972), pya.Point(480, 648)])
# polygon_id: p116
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p116)
p117 = pya.Polygon([pya.Point(168, 108), pya.Point(168, 432), pya.Point(264, 432), pya.Point(264, 108)])
# polygon_id: p117
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p117)
p118 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 972), pya.Point(264, 972), pya.Point(264, 648)])
# polygon_id: p118
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p118)
p119 = pya.Polygon([pya.Point(184, 108), pya.Point(184, 432), pya.Point(1112, 432), pya.Point(1112, 108)])
# polygon_id: p119
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p119)
p120 = pya.Polygon([pya.Point(184, 648), pya.Point(184, 972), pya.Point(1112, 972), pya.Point(1112, 648)])
# polygon_id: p120
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p120)
p121 = pya.Polygon([pya.Point(0, 40), pya.Point(0, 68), pya.Point(1296, 68), pya.Point(1296, 40)])
# polygon_id: p121
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p121)
p122 = pya.Polygon([pya.Point(0, 148), pya.Point(0, 176), pya.Point(1296, 176), pya.Point(1296, 148)])
# polygon_id: p122
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p122)
p123 = pya.Polygon([pya.Point(0, 256), pya.Point(0, 284), pya.Point(1296, 284), pya.Point(1296, 256)])
# polygon_id: p123
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p123)
p124 = pya.Polygon([pya.Point(0, 364), pya.Point(0, 392), pya.Point(1296, 392), pya.Point(1296, 364)])
# polygon_id: p124
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p124)
p125 = pya.Polygon([pya.Point(0, 472), pya.Point(0, 500), pya.Point(1296, 500), pya.Point(1296, 472)])
# polygon_id: p125
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p125)
p126 = pya.Polygon([pya.Point(0, 580), pya.Point(0, 608), pya.Point(1296, 608), pya.Point(1296, 580)])
# polygon_id: p126
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p126)
p127 = pya.Polygon([pya.Point(0, 688), pya.Point(0, 716), pya.Point(1296, 716), pya.Point(1296, 688)])
# polygon_id: p127
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p127)
p128 = pya.Polygon([pya.Point(0, 796), pya.Point(0, 824), pya.Point(1296, 824), pya.Point(1296, 796)])
# polygon_id: p128
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p128)
p129 = pya.Polygon([pya.Point(0, 904), pya.Point(0, 932), pya.Point(1296, 932), pya.Point(1296, 904)])
# polygon_id: p129
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p129)
p130 = pya.Polygon([pya.Point(0, 1012), pya.Point(0, 1040), pya.Point(1296, 1040), pya.Point(1296, 1012)])
# polygon_id: p130
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p130)
p131 = pya.Polygon([pya.Point(0, -32), pya.Point(0, 32), pya.Point(1296, 32), pya.Point(1296, -32)])
# polygon_id: p131
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p131)
p132 = pya.Polygon([pya.Point(0, 1048), pya.Point(0, 1112), pya.Point(1296, 1112), pya.Point(1296, 1048)])
# polygon_id: p132
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p132)
p133 = pya.Polygon([pya.Point(496, 496), pya.Point(496, 584), pya.Point(584, 584), pya.Point(584, 496)])
# polygon_id: p133
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p133)
p134 = pya.Polygon([pya.Point(712, 496), pya.Point(712, 584), pya.Point(800, 584), pya.Point(800, 496)])
# polygon_id: p134
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p134)
p135 = pya.Polygon([pya.Point(216, 496), pya.Point(216, 584), pya.Point(368, 584), pya.Point(368, 496)])
# polygon_id: p135
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p135)
p136 = pya.Polygon([pya.Point(928, 496), pya.Point(928, 584), pya.Point(1016, 584), pya.Point(1016, 496)])
# polygon_id: p136
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p136)
p137 = pya.Polygon([pya.Point(1044, -36), pya.Point(1044, 36), pya.Point(1116, 36), pya.Point(1116, -36)])
# polygon_id: p137
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p137)
p138 = pya.Polygon([pya.Point(1044, 108), pya.Point(1044, 180), pya.Point(1116, 180), pya.Point(1116, 108)])
# polygon_id: p138
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p138)
p139 = pya.Polygon([pya.Point(1044, 900), pya.Point(1044, 972), pya.Point(1116, 972), pya.Point(1116, 900)])
# polygon_id: p139
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p139)
p140 = pya.Polygon([pya.Point(1044, 1044), pya.Point(1044, 1116), pya.Point(1116, 1116), pya.Point(1116, 1044)])
# polygon_id: p140
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p140)
p141 = pya.Polygon([pya.Point(828, -36), pya.Point(828, 36), pya.Point(900, 36), pya.Point(900, -36)])
# polygon_id: p141
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p141)
p142 = pya.Polygon([pya.Point(828, 1044), pya.Point(828, 1116), pya.Point(900, 1116), pya.Point(900, 1044)])
# polygon_id: p142
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p142)
p143 = pya.Polygon([pya.Point(612, -36), pya.Point(612, 36), pya.Point(684, 36), pya.Point(684, -36)])
# polygon_id: p143
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p143)
p144 = pya.Polygon([pya.Point(612, 108), pya.Point(612, 180), pya.Point(684, 180), pya.Point(684, 108)])
# polygon_id: p144
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p144)
p145 = pya.Polygon([pya.Point(612, 900), pya.Point(612, 972), pya.Point(684, 972), pya.Point(684, 900)])
# polygon_id: p145
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p145)
p146 = pya.Polygon([pya.Point(612, 1044), pya.Point(612, 1116), pya.Point(684, 1116), pya.Point(684, 1044)])
# polygon_id: p146
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p146)
p147 = pya.Polygon([pya.Point(504, 504), pya.Point(504, 576), pya.Point(576, 576), pya.Point(576, 504)])
# polygon_id: p147
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p147)
p148 = pya.Polygon([pya.Point(396, -36), pya.Point(396, 36), pya.Point(468, 36), pya.Point(468, -36)])
# polygon_id: p148
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p148)
p149 = pya.Polygon([pya.Point(720, 504), pya.Point(720, 576), pya.Point(792, 576), pya.Point(792, 504)])
# polygon_id: p149
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p149)
p150 = pya.Polygon([pya.Point(396, 1044), pya.Point(396, 1116), pya.Point(468, 1116), pya.Point(468, 1044)])
# polygon_id: p150
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p150)
p151 = pya.Polygon([pya.Point(220, 504), pya.Point(220, 576), pya.Point(292, 576), pya.Point(292, 504)])
# polygon_id: p151
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p151)
p152 = pya.Polygon([pya.Point(180, -36), pya.Point(180, 36), pya.Point(252, 36), pya.Point(252, -36)])
# polygon_id: p152
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p152)
p153 = pya.Polygon([pya.Point(936, 504), pya.Point(936, 576), pya.Point(1008, 576), pya.Point(1008, 504)])
# polygon_id: p153
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p153)
p154 = pya.Polygon([pya.Point(180, 108), pya.Point(180, 180), pya.Point(252, 180), pya.Point(252, 108)])
# polygon_id: p154
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p154)
p155 = pya.Polygon([pya.Point(180, 900), pya.Point(180, 972), pya.Point(252, 972), pya.Point(252, 900)])
# polygon_id: p155
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p155)
p156 = pya.Polygon([pya.Point(180, 1044), pya.Point(180, 1116), pya.Point(252, 1116), pya.Point(252, 1044)])
# polygon_id: p156
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p156)
p157 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 540), pya.Point(1296, 540), pya.Point(1296, 0)])
# polygon_id: p157
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(12, 0))).insert(p157)
p158 = pya.Polygon([pya.Point(1080, 452), pya.Point(1080, 628), pya.Point(1296, 628), pya.Point(1296, 452)])
# polygon_id: p158
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p158)
p159 = pya.Polygon([pya.Point(0, 992), pya.Point(0, 1168), pya.Point(1296, 1168), pya.Point(1296, 992)])
# polygon_id: p159
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p159)
p160 = pya.Polygon([pya.Point(0, 452), pya.Point(0, 628), pya.Point(216, 628), pya.Point(216, 452)])
# polygon_id: p160
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p160)
p161 = pya.Polygon([pya.Point(0, -88), pya.Point(0, 88), pya.Point(1296, 88), pya.Point(1296, -88)])
# polygon_id: p161
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p161)
p162 = pya.Polygon([pya.Point(1148, -20), pya.Point(1148, 1102), pya.Point(1228, 1102), pya.Point(1228, -20)])
# polygon_id: p162
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p162)
p163 = pya.Polygon([pya.Point(932, -20), pya.Point(932, 1102), pya.Point(1012, 1102), pya.Point(1012, -20)])
# polygon_id: p163
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p163)
p164 = pya.Polygon([pya.Point(716, -20), pya.Point(716, 1102), pya.Point(796, 1102), pya.Point(796, -20)])
# polygon_id: p164
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p164)
p165 = pya.Polygon([pya.Point(500, -20), pya.Point(500, 1102), pya.Point(580, 1102), pya.Point(580, -20)])
# polygon_id: p165
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p165)
p166 = pya.Polygon([pya.Point(284, -20), pya.Point(284, 1102), pya.Point(364, 1102), pya.Point(364, -20)])
# polygon_id: p166
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p166)
p167 = pya.Polygon([pya.Point(68, -20), pya.Point(68, 1102), pya.Point(148, 1102), pya.Point(148, -20)])
# polygon_id: p167
cell_BUFx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p167)
p174 = pya.Polygon([pya.Point(376, 108), pya.Point(376, 180), pya.Point(1044, 180), pya.Point(1044, 900), pya.Point(376, 900), pya.Point(376, 972), pya.Point(1116, 972), pya.Point(1116, 576), pya.Point(1244, 576), pya.Point(1244, 504), pya.Point(1116, 504), pya.Point(1116, 108)])
# polygon_id: p174
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p174)
p175 = pya.Polygon([pya.Point(1240, 108), pya.Point(1240, 180), pya.Point(3744, 180), pya.Point(3744, 900), pya.Point(1240, 900), pya.Point(1240, 972), pya.Point(3816, 972), pya.Point(3816, 108)])
# polygon_id: p175
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p175)
p176 = pya.Polygon([pya.Point(72, 136), pya.Point(72, 944), pya.Point(144, 944), pya.Point(144, 576), pya.Point(296, 576), pya.Point(296, 504), pya.Point(144, 504), pya.Point(144, 136)])
# polygon_id: p176
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p176)
p177 = pya.Polygon([pya.Point(0, 1044), pya.Point(0, 1116), pya.Point(3888, 1116), pya.Point(3888, 1044)])
# polygon_id: p177
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p177)
p178 = pya.Polygon([pya.Point(0, -36), pya.Point(0, 36), pya.Point(3888, 36), pya.Point(3888, -36)])
# polygon_id: p178
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p178)
p179 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(3888, 1080), pya.Point(3888, 540)])
# polygon_id: p179
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(13, 0))).insert(p179)
p180 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(3888, 1080), pya.Point(3888, 540)])
# polygon_id: p180
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(1, 0))).insert(p180)
p181 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 1080), pya.Point(3888, 1080), pya.Point(3888, 0)])
# polygon_id: p181
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(100, 0))).insert(p181)
p182 = pya.Polygon([pya.Point(3624, 0), pya.Point(3624, 432), pya.Point(3720, 432), pya.Point(3720, 0)])
# polygon_id: p182
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p182)
p183 = pya.Polygon([pya.Point(3624, 648), pya.Point(3624, 1080), pya.Point(3720, 1080), pya.Point(3720, 648)])
# polygon_id: p183
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p183)
p184 = pya.Polygon([pya.Point(3408, 108), pya.Point(3408, 432), pya.Point(3504, 432), pya.Point(3504, 108)])
# polygon_id: p184
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p184)
p185 = pya.Polygon([pya.Point(3408, 648), pya.Point(3408, 972), pya.Point(3504, 972), pya.Point(3504, 648)])
# polygon_id: p185
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p185)
p186 = pya.Polygon([pya.Point(3192, 0), pya.Point(3192, 432), pya.Point(3288, 432), pya.Point(3288, 0)])
# polygon_id: p186
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p186)
p187 = pya.Polygon([pya.Point(3192, 648), pya.Point(3192, 1080), pya.Point(3288, 1080), pya.Point(3288, 648)])
# polygon_id: p187
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p187)
p188 = pya.Polygon([pya.Point(2976, 108), pya.Point(2976, 432), pya.Point(3072, 432), pya.Point(3072, 108)])
# polygon_id: p188
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p188)
p189 = pya.Polygon([pya.Point(2976, 648), pya.Point(2976, 972), pya.Point(3072, 972), pya.Point(3072, 648)])
# polygon_id: p189
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p189)
p190 = pya.Polygon([pya.Point(2760, 0), pya.Point(2760, 432), pya.Point(2856, 432), pya.Point(2856, 0)])
# polygon_id: p190
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p190)
p191 = pya.Polygon([pya.Point(2760, 648), pya.Point(2760, 1080), pya.Point(2856, 1080), pya.Point(2856, 648)])
# polygon_id: p191
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p191)
p192 = pya.Polygon([pya.Point(2544, 108), pya.Point(2544, 432), pya.Point(2640, 432), pya.Point(2640, 108)])
# polygon_id: p192
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p192)
p193 = pya.Polygon([pya.Point(2544, 648), pya.Point(2544, 972), pya.Point(2640, 972), pya.Point(2640, 648)])
# polygon_id: p193
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p193)
p194 = pya.Polygon([pya.Point(2328, 0), pya.Point(2328, 432), pya.Point(2424, 432), pya.Point(2424, 0)])
# polygon_id: p194
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p194)
p195 = pya.Polygon([pya.Point(2328, 648), pya.Point(2328, 1080), pya.Point(2424, 1080), pya.Point(2424, 648)])
# polygon_id: p195
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p195)
p196 = pya.Polygon([pya.Point(2112, 108), pya.Point(2112, 432), pya.Point(2208, 432), pya.Point(2208, 108)])
# polygon_id: p196
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p196)
p197 = pya.Polygon([pya.Point(2112, 648), pya.Point(2112, 972), pya.Point(2208, 972), pya.Point(2208, 648)])
# polygon_id: p197
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p197)
p198 = pya.Polygon([pya.Point(1896, 0), pya.Point(1896, 432), pya.Point(1992, 432), pya.Point(1992, 0)])
# polygon_id: p198
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p198)
p199 = pya.Polygon([pya.Point(1896, 648), pya.Point(1896, 1080), pya.Point(1992, 1080), pya.Point(1992, 648)])
# polygon_id: p199
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p199)
p200 = pya.Polygon([pya.Point(1680, 108), pya.Point(1680, 432), pya.Point(1776, 432), pya.Point(1776, 108)])
# polygon_id: p200
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p200)
p201 = pya.Polygon([pya.Point(1680, 648), pya.Point(1680, 972), pya.Point(1776, 972), pya.Point(1776, 648)])
# polygon_id: p201
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p201)
p202 = pya.Polygon([pya.Point(1464, 0), pya.Point(1464, 432), pya.Point(1560, 432), pya.Point(1560, 0)])
# polygon_id: p202
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p202)
p203 = pya.Polygon([pya.Point(1464, 648), pya.Point(1464, 1080), pya.Point(1560, 1080), pya.Point(1560, 648)])
# polygon_id: p203
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p203)
p204 = pya.Polygon([pya.Point(1248, 108), pya.Point(1248, 432), pya.Point(1344, 432), pya.Point(1344, 108)])
# polygon_id: p204
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p204)
p205 = pya.Polygon([pya.Point(1248, 648), pya.Point(1248, 972), pya.Point(1344, 972), pya.Point(1344, 648)])
# polygon_id: p205
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p205)
p206 = pya.Polygon([pya.Point(1032, 0), pya.Point(1032, 432), pya.Point(1128, 432), pya.Point(1128, 0)])
# polygon_id: p206
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p206)
p207 = pya.Polygon([pya.Point(1032, 648), pya.Point(1032, 1080), pya.Point(1128, 1080), pya.Point(1128, 648)])
# polygon_id: p207
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p207)
p208 = pya.Polygon([pya.Point(816, 108), pya.Point(816, 432), pya.Point(912, 432), pya.Point(912, 108)])
# polygon_id: p208
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p208)
p209 = pya.Polygon([pya.Point(816, 648), pya.Point(816, 972), pya.Point(912, 972), pya.Point(912, 648)])
# polygon_id: p209
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p209)
p210 = pya.Polygon([pya.Point(600, 0), pya.Point(600, 432), pya.Point(696, 432), pya.Point(696, 0)])
# polygon_id: p210
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p210)
p211 = pya.Polygon([pya.Point(600, 648), pya.Point(600, 1080), pya.Point(696, 1080), pya.Point(696, 648)])
# polygon_id: p211
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p211)
p212 = pya.Polygon([pya.Point(384, 108), pya.Point(384, 432), pya.Point(480, 432), pya.Point(480, 108)])
# polygon_id: p212
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p212)
p213 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 972), pya.Point(480, 972), pya.Point(480, 648)])
# polygon_id: p213
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p213)
p214 = pya.Polygon([pya.Point(168, 0), pya.Point(168, 432), pya.Point(264, 432), pya.Point(264, 0)])
# polygon_id: p214
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p214)
p215 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 1080), pya.Point(264, 1080), pya.Point(264, 648)])
# polygon_id: p215
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p215)
p216 = pya.Polygon([pya.Point(3624, 108), pya.Point(3624, 432), pya.Point(3720, 432), pya.Point(3720, 108)])
# polygon_id: p216
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p216)
p217 = pya.Polygon([pya.Point(3624, 648), pya.Point(3624, 972), pya.Point(3720, 972), pya.Point(3720, 648)])
# polygon_id: p217
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p217)
p218 = pya.Polygon([pya.Point(3408, 108), pya.Point(3408, 432), pya.Point(3504, 432), pya.Point(3504, 108)])
# polygon_id: p218
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p218)
p219 = pya.Polygon([pya.Point(3408, 648), pya.Point(3408, 972), pya.Point(3504, 972), pya.Point(3504, 648)])
# polygon_id: p219
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p219)
p220 = pya.Polygon([pya.Point(3192, 108), pya.Point(3192, 432), pya.Point(3288, 432), pya.Point(3288, 108)])
# polygon_id: p220
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p220)
p221 = pya.Polygon([pya.Point(3192, 648), pya.Point(3192, 972), pya.Point(3288, 972), pya.Point(3288, 648)])
# polygon_id: p221
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p221)
p222 = pya.Polygon([pya.Point(2976, 108), pya.Point(2976, 432), pya.Point(3072, 432), pya.Point(3072, 108)])
# polygon_id: p222
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p222)
p223 = pya.Polygon([pya.Point(2976, 648), pya.Point(2976, 972), pya.Point(3072, 972), pya.Point(3072, 648)])
# polygon_id: p223
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p223)
p224 = pya.Polygon([pya.Point(2760, 108), pya.Point(2760, 432), pya.Point(2856, 432), pya.Point(2856, 108)])
# polygon_id: p224
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p224)
p225 = pya.Polygon([pya.Point(2760, 648), pya.Point(2760, 972), pya.Point(2856, 972), pya.Point(2856, 648)])
# polygon_id: p225
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p225)
p226 = pya.Polygon([pya.Point(2544, 108), pya.Point(2544, 432), pya.Point(2640, 432), pya.Point(2640, 108)])
# polygon_id: p226
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p226)
p227 = pya.Polygon([pya.Point(2544, 648), pya.Point(2544, 972), pya.Point(2640, 972), pya.Point(2640, 648)])
# polygon_id: p227
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p227)
p228 = pya.Polygon([pya.Point(2328, 108), pya.Point(2328, 432), pya.Point(2424, 432), pya.Point(2424, 108)])
# polygon_id: p228
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p228)
p229 = pya.Polygon([pya.Point(2328, 648), pya.Point(2328, 972), pya.Point(2424, 972), pya.Point(2424, 648)])
# polygon_id: p229
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p229)
p230 = pya.Polygon([pya.Point(2112, 108), pya.Point(2112, 432), pya.Point(2208, 432), pya.Point(2208, 108)])
# polygon_id: p230
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p230)
p231 = pya.Polygon([pya.Point(2112, 648), pya.Point(2112, 972), pya.Point(2208, 972), pya.Point(2208, 648)])
# polygon_id: p231
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p231)
p232 = pya.Polygon([pya.Point(1896, 108), pya.Point(1896, 432), pya.Point(1992, 432), pya.Point(1992, 108)])
# polygon_id: p232
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p232)
p233 = pya.Polygon([pya.Point(1896, 648), pya.Point(1896, 972), pya.Point(1992, 972), pya.Point(1992, 648)])
# polygon_id: p233
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p233)
p234 = pya.Polygon([pya.Point(1680, 108), pya.Point(1680, 432), pya.Point(1776, 432), pya.Point(1776, 108)])
# polygon_id: p234
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p234)
p235 = pya.Polygon([pya.Point(1680, 648), pya.Point(1680, 972), pya.Point(1776, 972), pya.Point(1776, 648)])
# polygon_id: p235
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p235)
p236 = pya.Polygon([pya.Point(1464, 108), pya.Point(1464, 432), pya.Point(1560, 432), pya.Point(1560, 108)])
# polygon_id: p236
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p236)
p237 = pya.Polygon([pya.Point(1464, 648), pya.Point(1464, 972), pya.Point(1560, 972), pya.Point(1560, 648)])
# polygon_id: p237
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p237)
p238 = pya.Polygon([pya.Point(1248, 108), pya.Point(1248, 432), pya.Point(1344, 432), pya.Point(1344, 108)])
# polygon_id: p238
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p238)
p239 = pya.Polygon([pya.Point(1248, 648), pya.Point(1248, 972), pya.Point(1344, 972), pya.Point(1344, 648)])
# polygon_id: p239
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p239)
p240 = pya.Polygon([pya.Point(1032, 108), pya.Point(1032, 432), pya.Point(1128, 432), pya.Point(1128, 108)])
# polygon_id: p240
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p240)
p241 = pya.Polygon([pya.Point(1032, 648), pya.Point(1032, 972), pya.Point(1128, 972), pya.Point(1128, 648)])
# polygon_id: p241
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p241)
p242 = pya.Polygon([pya.Point(816, 108), pya.Point(816, 432), pya.Point(912, 432), pya.Point(912, 108)])
# polygon_id: p242
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p242)
p243 = pya.Polygon([pya.Point(816, 648), pya.Point(816, 972), pya.Point(912, 972), pya.Point(912, 648)])
# polygon_id: p243
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p243)
p244 = pya.Polygon([pya.Point(600, 108), pya.Point(600, 432), pya.Point(696, 432), pya.Point(696, 108)])
# polygon_id: p244
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p244)
p245 = pya.Polygon([pya.Point(600, 648), pya.Point(600, 972), pya.Point(696, 972), pya.Point(696, 648)])
# polygon_id: p245
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p245)
p246 = pya.Polygon([pya.Point(384, 108), pya.Point(384, 432), pya.Point(480, 432), pya.Point(480, 108)])
# polygon_id: p246
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p246)
p247 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 972), pya.Point(480, 972), pya.Point(480, 648)])
# polygon_id: p247
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p247)
p248 = pya.Polygon([pya.Point(168, 108), pya.Point(168, 432), pya.Point(264, 432), pya.Point(264, 108)])
# polygon_id: p248
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p248)
p249 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 972), pya.Point(264, 972), pya.Point(264, 648)])
# polygon_id: p249
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p249)
p250 = pya.Polygon([pya.Point(184, 108), pya.Point(184, 432), pya.Point(3704, 432), pya.Point(3704, 108)])
# polygon_id: p250
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p250)
p251 = pya.Polygon([pya.Point(184, 648), pya.Point(184, 972), pya.Point(3704, 972), pya.Point(3704, 648)])
# polygon_id: p251
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p251)
p252 = pya.Polygon([pya.Point(0, 40), pya.Point(0, 68), pya.Point(3888, 68), pya.Point(3888, 40)])
# polygon_id: p252
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p252)
p253 = pya.Polygon([pya.Point(0, 148), pya.Point(0, 176), pya.Point(3888, 176), pya.Point(3888, 148)])
# polygon_id: p253
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p253)
p254 = pya.Polygon([pya.Point(0, 256), pya.Point(0, 284), pya.Point(3888, 284), pya.Point(3888, 256)])
# polygon_id: p254
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p254)
p255 = pya.Polygon([pya.Point(0, 364), pya.Point(0, 392), pya.Point(3888, 392), pya.Point(3888, 364)])
# polygon_id: p255
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p255)
p256 = pya.Polygon([pya.Point(0, 472), pya.Point(0, 500), pya.Point(3888, 500), pya.Point(3888, 472)])
# polygon_id: p256
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p256)
p257 = pya.Polygon([pya.Point(0, 580), pya.Point(0, 608), pya.Point(3888, 608), pya.Point(3888, 580)])
# polygon_id: p257
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p257)
p258 = pya.Polygon([pya.Point(0, 688), pya.Point(0, 716), pya.Point(3888, 716), pya.Point(3888, 688)])
# polygon_id: p258
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p258)
p259 = pya.Polygon([pya.Point(0, 796), pya.Point(0, 824), pya.Point(3888, 824), pya.Point(3888, 796)])
# polygon_id: p259
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p259)
p260 = pya.Polygon([pya.Point(0, 904), pya.Point(0, 932), pya.Point(3888, 932), pya.Point(3888, 904)])
# polygon_id: p260
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p260)
p261 = pya.Polygon([pya.Point(0, 1012), pya.Point(0, 1040), pya.Point(3888, 1040), pya.Point(3888, 1012)])
# polygon_id: p261
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p261)
p262 = pya.Polygon([pya.Point(0, -32), pya.Point(0, 32), pya.Point(3888, 32), pya.Point(3888, -32)])
# polygon_id: p262
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p262)
p263 = pya.Polygon([pya.Point(0, 1048), pya.Point(0, 1112), pya.Point(3888, 1112), pya.Point(3888, 1048)])
# polygon_id: p263
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p263)
p264 = pya.Polygon([pya.Point(1140, 496), pya.Point(1140, 584), pya.Point(3620, 584), pya.Point(3620, 496)])
# polygon_id: p264
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p264)
p265 = pya.Polygon([pya.Point(200, 496), pya.Point(200, 584), pya.Point(1016, 584), pya.Point(1016, 496)])
# polygon_id: p265
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p265)
p266 = pya.Polygon([pya.Point(3636, -36), pya.Point(3636, 36), pya.Point(3708, 36), pya.Point(3708, -36)])
# polygon_id: p266
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p266)
p267 = pya.Polygon([pya.Point(3636, 1044), pya.Point(3636, 1116), pya.Point(3708, 1116), pya.Point(3708, 1044)])
# polygon_id: p267
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p267)
p268 = pya.Polygon([pya.Point(3420, -36), pya.Point(3420, 36), pya.Point(3492, 36), pya.Point(3492, -36)])
# polygon_id: p268
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p268)
p269 = pya.Polygon([pya.Point(3420, 108), pya.Point(3420, 180), pya.Point(3492, 180), pya.Point(3492, 108)])
# polygon_id: p269
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p269)
p270 = pya.Polygon([pya.Point(3420, 900), pya.Point(3420, 972), pya.Point(3492, 972), pya.Point(3492, 900)])
# polygon_id: p270
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p270)
p271 = pya.Polygon([pya.Point(3420, 1044), pya.Point(3420, 1116), pya.Point(3492, 1116), pya.Point(3492, 1044)])
# polygon_id: p271
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p271)
p272 = pya.Polygon([pya.Point(3204, -36), pya.Point(3204, 36), pya.Point(3276, 36), pya.Point(3276, -36)])
# polygon_id: p272
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p272)
p273 = pya.Polygon([pya.Point(3204, 1044), pya.Point(3204, 1116), pya.Point(3276, 1116), pya.Point(3276, 1044)])
# polygon_id: p273
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p273)
p274 = pya.Polygon([pya.Point(2988, -36), pya.Point(2988, 36), pya.Point(3060, 36), pya.Point(3060, -36)])
# polygon_id: p274
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p274)
p275 = pya.Polygon([pya.Point(2988, 108), pya.Point(2988, 180), pya.Point(3060, 180), pya.Point(3060, 108)])
# polygon_id: p275
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p275)
p276 = pya.Polygon([pya.Point(2988, 900), pya.Point(2988, 972), pya.Point(3060, 972), pya.Point(3060, 900)])
# polygon_id: p276
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p276)
p277 = pya.Polygon([pya.Point(2988, 1044), pya.Point(2988, 1116), pya.Point(3060, 1116), pya.Point(3060, 1044)])
# polygon_id: p277
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p277)
p278 = pya.Polygon([pya.Point(2772, -36), pya.Point(2772, 36), pya.Point(2844, 36), pya.Point(2844, -36)])
# polygon_id: p278
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p278)
p279 = pya.Polygon([pya.Point(2772, 1044), pya.Point(2772, 1116), pya.Point(2844, 1116), pya.Point(2844, 1044)])
# polygon_id: p279
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p279)
p280 = pya.Polygon([pya.Point(2556, -36), pya.Point(2556, 36), pya.Point(2628, 36), pya.Point(2628, -36)])
# polygon_id: p280
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p280)
p281 = pya.Polygon([pya.Point(2556, 108), pya.Point(2556, 180), pya.Point(2628, 180), pya.Point(2628, 108)])
# polygon_id: p281
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p281)
p282 = pya.Polygon([pya.Point(2556, 900), pya.Point(2556, 972), pya.Point(2628, 972), pya.Point(2628, 900)])
# polygon_id: p282
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p282)
p283 = pya.Polygon([pya.Point(2556, 1044), pya.Point(2556, 1116), pya.Point(2628, 1116), pya.Point(2628, 1044)])
# polygon_id: p283
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p283)
p284 = pya.Polygon([pya.Point(2340, -36), pya.Point(2340, 36), pya.Point(2412, 36), pya.Point(2412, -36)])
# polygon_id: p284
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p284)
p285 = pya.Polygon([pya.Point(2340, 1044), pya.Point(2340, 1116), pya.Point(2412, 1116), pya.Point(2412, 1044)])
# polygon_id: p285
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p285)
p286 = pya.Polygon([pya.Point(2124, -36), pya.Point(2124, 36), pya.Point(2196, 36), pya.Point(2196, -36)])
# polygon_id: p286
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p286)
p287 = pya.Polygon([pya.Point(2124, 108), pya.Point(2124, 180), pya.Point(2196, 180), pya.Point(2196, 108)])
# polygon_id: p287
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p287)
p288 = pya.Polygon([pya.Point(2124, 900), pya.Point(2124, 972), pya.Point(2196, 972), pya.Point(2196, 900)])
# polygon_id: p288
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p288)
p289 = pya.Polygon([pya.Point(2124, 1044), pya.Point(2124, 1116), pya.Point(2196, 1116), pya.Point(2196, 1044)])
# polygon_id: p289
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p289)
p290 = pya.Polygon([pya.Point(1908, -36), pya.Point(1908, 36), pya.Point(1980, 36), pya.Point(1980, -36)])
# polygon_id: p290
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p290)
p291 = pya.Polygon([pya.Point(1908, 1044), pya.Point(1908, 1116), pya.Point(1980, 1116), pya.Point(1980, 1044)])
# polygon_id: p291
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p291)
p292 = pya.Polygon([pya.Point(1692, -36), pya.Point(1692, 36), pya.Point(1764, 36), pya.Point(1764, -36)])
# polygon_id: p292
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p292)
p293 = pya.Polygon([pya.Point(1692, 108), pya.Point(1692, 180), pya.Point(1764, 180), pya.Point(1764, 108)])
# polygon_id: p293
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p293)
p294 = pya.Polygon([pya.Point(1692, 900), pya.Point(1692, 972), pya.Point(1764, 972), pya.Point(1764, 900)])
# polygon_id: p294
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p294)
p295 = pya.Polygon([pya.Point(1692, 1044), pya.Point(1692, 1116), pya.Point(1764, 1116), pya.Point(1764, 1044)])
# polygon_id: p295
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p295)
p296 = pya.Polygon([pya.Point(1476, -36), pya.Point(1476, 36), pya.Point(1548, 36), pya.Point(1548, -36)])
# polygon_id: p296
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p296)
p297 = pya.Polygon([pya.Point(1476, 1044), pya.Point(1476, 1116), pya.Point(1548, 1116), pya.Point(1548, 1044)])
# polygon_id: p297
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p297)
p298 = pya.Polygon([pya.Point(1260, -36), pya.Point(1260, 36), pya.Point(1332, 36), pya.Point(1332, -36)])
# polygon_id: p298
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p298)
p299 = pya.Polygon([pya.Point(1260, 108), pya.Point(1260, 180), pya.Point(1332, 180), pya.Point(1332, 108)])
# polygon_id: p299
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p299)
p300 = pya.Polygon([pya.Point(1260, 900), pya.Point(1260, 972), pya.Point(1332, 972), pya.Point(1332, 900)])
# polygon_id: p300
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p300)
p301 = pya.Polygon([pya.Point(1260, 1044), pya.Point(1260, 1116), pya.Point(1332, 1116), pya.Point(1332, 1044)])
# polygon_id: p301
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p301)
p302 = pya.Polygon([pya.Point(1152, 504), pya.Point(1152, 576), pya.Point(1224, 576), pya.Point(1224, 504)])
# polygon_id: p302
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p302)
p303 = pya.Polygon([pya.Point(1044, -36), pya.Point(1044, 36), pya.Point(1116, 36), pya.Point(1116, -36)])
# polygon_id: p303
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p303)
p304 = pya.Polygon([pya.Point(1044, 1044), pya.Point(1044, 1116), pya.Point(1116, 1116), pya.Point(1116, 1044)])
# polygon_id: p304
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p304)
p305 = pya.Polygon([pya.Point(828, -36), pya.Point(828, 36), pya.Point(900, 36), pya.Point(900, -36)])
# polygon_id: p305
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p305)
p306 = pya.Polygon([pya.Point(828, 108), pya.Point(828, 180), pya.Point(900, 180), pya.Point(900, 108)])
# polygon_id: p306
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p306)
p307 = pya.Polygon([pya.Point(828, 900), pya.Point(828, 972), pya.Point(900, 972), pya.Point(900, 900)])
# polygon_id: p307
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p307)
p308 = pya.Polygon([pya.Point(828, 1044), pya.Point(828, 1116), pya.Point(900, 1116), pya.Point(900, 1044)])
# polygon_id: p308
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p308)
p309 = pya.Polygon([pya.Point(612, -36), pya.Point(612, 36), pya.Point(684, 36), pya.Point(684, -36)])
# polygon_id: p309
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p309)
p310 = pya.Polygon([pya.Point(612, 1044), pya.Point(612, 1116), pya.Point(684, 1116), pya.Point(684, 1044)])
# polygon_id: p310
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p310)
p311 = pya.Polygon([pya.Point(396, -36), pya.Point(396, 36), pya.Point(468, 36), pya.Point(468, -36)])
# polygon_id: p311
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p311)
p312 = pya.Polygon([pya.Point(396, 108), pya.Point(396, 180), pya.Point(468, 180), pya.Point(468, 108)])
# polygon_id: p312
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p312)
p313 = pya.Polygon([pya.Point(396, 900), pya.Point(396, 972), pya.Point(468, 972), pya.Point(468, 900)])
# polygon_id: p313
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p313)
p314 = pya.Polygon([pya.Point(396, 1044), pya.Point(396, 1116), pya.Point(468, 1116), pya.Point(468, 1044)])
# polygon_id: p314
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p314)
p315 = pya.Polygon([pya.Point(204, 504), pya.Point(204, 576), pya.Point(276, 576), pya.Point(276, 504)])
# polygon_id: p315
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p315)
p316 = pya.Polygon([pya.Point(180, -36), pya.Point(180, 36), pya.Point(252, 36), pya.Point(252, -36)])
# polygon_id: p316
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p316)
p317 = pya.Polygon([pya.Point(180, 1044), pya.Point(180, 1116), pya.Point(252, 1116), pya.Point(252, 1044)])
# polygon_id: p317
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p317)
p318 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 540), pya.Point(3888, 540), pya.Point(3888, 0)])
# polygon_id: p318
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(12, 0))).insert(p318)
p319 = pya.Polygon([pya.Point(0, -88), pya.Point(0, 88), pya.Point(3888, 88), pya.Point(3888, -88)])
# polygon_id: p319
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p319)
p320 = pya.Polygon([pya.Point(3672, 452), pya.Point(3672, 628), pya.Point(3888, 628), pya.Point(3888, 452)])
# polygon_id: p320
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p320)
p321 = pya.Polygon([pya.Point(0, 992), pya.Point(0, 1168), pya.Point(3888, 1168), pya.Point(3888, 992)])
# polygon_id: p321
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p321)
p322 = pya.Polygon([pya.Point(0, 452), pya.Point(0, 628), pya.Point(216, 628), pya.Point(216, 452)])
# polygon_id: p322
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p322)
p323 = pya.Polygon([pya.Point(3740, -20), pya.Point(3740, 1102), pya.Point(3820, 1102), pya.Point(3820, -20)])
# polygon_id: p323
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p323)
p324 = pya.Polygon([pya.Point(3524, -20), pya.Point(3524, 1102), pya.Point(3604, 1102), pya.Point(3604, -20)])
# polygon_id: p324
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p324)
p325 = pya.Polygon([pya.Point(3308, -20), pya.Point(3308, 1102), pya.Point(3388, 1102), pya.Point(3388, -20)])
# polygon_id: p325
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p325)
p326 = pya.Polygon([pya.Point(3092, -20), pya.Point(3092, 1102), pya.Point(3172, 1102), pya.Point(3172, -20)])
# polygon_id: p326
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p326)
p327 = pya.Polygon([pya.Point(2876, -20), pya.Point(2876, 1102), pya.Point(2956, 1102), pya.Point(2956, -20)])
# polygon_id: p327
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p327)
p328 = pya.Polygon([pya.Point(2660, -20), pya.Point(2660, 1102), pya.Point(2740, 1102), pya.Point(2740, -20)])
# polygon_id: p328
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p328)
p329 = pya.Polygon([pya.Point(2444, -20), pya.Point(2444, 1102), pya.Point(2524, 1102), pya.Point(2524, -20)])
# polygon_id: p329
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p329)
p330 = pya.Polygon([pya.Point(2228, -20), pya.Point(2228, 1102), pya.Point(2308, 1102), pya.Point(2308, -20)])
# polygon_id: p330
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p330)
p331 = pya.Polygon([pya.Point(2012, -20), pya.Point(2012, 1102), pya.Point(2092, 1102), pya.Point(2092, -20)])
# polygon_id: p331
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p331)
p332 = pya.Polygon([pya.Point(1796, -20), pya.Point(1796, 1102), pya.Point(1876, 1102), pya.Point(1876, -20)])
# polygon_id: p332
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p332)
p333 = pya.Polygon([pya.Point(1580, -20), pya.Point(1580, 1102), pya.Point(1660, 1102), pya.Point(1660, -20)])
# polygon_id: p333
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p333)
p334 = pya.Polygon([pya.Point(1364, -20), pya.Point(1364, 1102), pya.Point(1444, 1102), pya.Point(1444, -20)])
# polygon_id: p334
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p334)
p335 = pya.Polygon([pya.Point(1148, -20), pya.Point(1148, 1102), pya.Point(1228, 1102), pya.Point(1228, -20)])
# polygon_id: p335
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p335)
p336 = pya.Polygon([pya.Point(932, -20), pya.Point(932, 1102), pya.Point(1012, 1102), pya.Point(1012, -20)])
# polygon_id: p336
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p336)
p337 = pya.Polygon([pya.Point(716, -20), pya.Point(716, 1102), pya.Point(796, 1102), pya.Point(796, -20)])
# polygon_id: p337
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p337)
p338 = pya.Polygon([pya.Point(500, -20), pya.Point(500, 1102), pya.Point(580, 1102), pya.Point(580, -20)])
# polygon_id: p338
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p338)
p339 = pya.Polygon([pya.Point(284, -20), pya.Point(284, 1102), pya.Point(364, 1102), pya.Point(364, -20)])
# polygon_id: p339
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p339)
p340 = pya.Polygon([pya.Point(68, -20), pya.Point(68, 1102), pya.Point(148, 1102), pya.Point(148, -20)])
# polygon_id: p340
cell_BUFx12f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p340)
p347 = pya.Polygon([pya.Point(72, 136), pya.Point(72, 944), pya.Point(144, 944), pya.Point(144, 576), pya.Point(336, 576), pya.Point(336, 504), pya.Point(144, 504), pya.Point(144, 136)])
# polygon_id: p347
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p347)
p348 = pya.Polygon([pya.Point(376, 108), pya.Point(376, 180), pya.Point(504, 180), pya.Point(504, 900), pya.Point(376, 900), pya.Point(376, 972), pya.Point(576, 972), pya.Point(576, 576), pya.Point(1892, 576), pya.Point(1892, 504), pya.Point(576, 504), pya.Point(576, 108)])
# polygon_id: p348
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p348)
p349 = pya.Polygon([pya.Point(808, 108), pya.Point(808, 180), pya.Point(2016, 180), pya.Point(2016, 900), pya.Point(808, 900), pya.Point(808, 972), pya.Point(2088, 972), pya.Point(2088, 108)])
# polygon_id: p349
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p349)
p350 = pya.Polygon([pya.Point(0, 1044), pya.Point(0, 1116), pya.Point(2160, 1116), pya.Point(2160, 1044)])
# polygon_id: p350
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p350)
p351 = pya.Polygon([pya.Point(0, -36), pya.Point(0, 36), pya.Point(2160, 36), pya.Point(2160, -36)])
# polygon_id: p351
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p351)
p352 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(2160, 1080), pya.Point(2160, 540)])
# polygon_id: p352
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(13, 0))).insert(p352)
p353 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(2160, 1080), pya.Point(2160, 540)])
# polygon_id: p353
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(1, 0))).insert(p353)
p354 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 1080), pya.Point(2160, 1080), pya.Point(2160, 0)])
# polygon_id: p354
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(100, 0))).insert(p354)
p355 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 1080), pya.Point(264, 1080), pya.Point(264, 648)])
# polygon_id: p355
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p355)
p356 = pya.Polygon([pya.Point(168, 0), pya.Point(168, 432), pya.Point(264, 432), pya.Point(264, 0)])
# polygon_id: p356
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p356)
p357 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 972), pya.Point(480, 972), pya.Point(480, 648)])
# polygon_id: p357
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p357)
p358 = pya.Polygon([pya.Point(384, 108), pya.Point(384, 432), pya.Point(480, 432), pya.Point(480, 108)])
# polygon_id: p358
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p358)
p359 = pya.Polygon([pya.Point(600, 648), pya.Point(600, 1080), pya.Point(696, 1080), pya.Point(696, 648)])
# polygon_id: p359
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p359)
p360 = pya.Polygon([pya.Point(600, 0), pya.Point(600, 432), pya.Point(696, 432), pya.Point(696, 0)])
# polygon_id: p360
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p360)
p361 = pya.Polygon([pya.Point(816, 648), pya.Point(816, 972), pya.Point(912, 972), pya.Point(912, 648)])
# polygon_id: p361
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p361)
p362 = pya.Polygon([pya.Point(816, 108), pya.Point(816, 432), pya.Point(912, 432), pya.Point(912, 108)])
# polygon_id: p362
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p362)
p363 = pya.Polygon([pya.Point(1032, 648), pya.Point(1032, 1080), pya.Point(1128, 1080), pya.Point(1128, 648)])
# polygon_id: p363
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p363)
p364 = pya.Polygon([pya.Point(1032, 0), pya.Point(1032, 432), pya.Point(1128, 432), pya.Point(1128, 0)])
# polygon_id: p364
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p364)
p365 = pya.Polygon([pya.Point(1248, 648), pya.Point(1248, 972), pya.Point(1344, 972), pya.Point(1344, 648)])
# polygon_id: p365
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p365)
p366 = pya.Polygon([pya.Point(1248, 108), pya.Point(1248, 432), pya.Point(1344, 432), pya.Point(1344, 108)])
# polygon_id: p366
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p366)
p367 = pya.Polygon([pya.Point(1464, 648), pya.Point(1464, 1080), pya.Point(1560, 1080), pya.Point(1560, 648)])
# polygon_id: p367
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p367)
p368 = pya.Polygon([pya.Point(1464, 0), pya.Point(1464, 432), pya.Point(1560, 432), pya.Point(1560, 0)])
# polygon_id: p368
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p368)
p369 = pya.Polygon([pya.Point(1680, 648), pya.Point(1680, 972), pya.Point(1776, 972), pya.Point(1776, 648)])
# polygon_id: p369
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p369)
p370 = pya.Polygon([pya.Point(1680, 108), pya.Point(1680, 432), pya.Point(1776, 432), pya.Point(1776, 108)])
# polygon_id: p370
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p370)
p371 = pya.Polygon([pya.Point(1896, 648), pya.Point(1896, 1080), pya.Point(1992, 1080), pya.Point(1992, 648)])
# polygon_id: p371
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p371)
p372 = pya.Polygon([pya.Point(1896, 0), pya.Point(1896, 432), pya.Point(1992, 432), pya.Point(1992, 0)])
# polygon_id: p372
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p372)
p373 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 972), pya.Point(264, 972), pya.Point(264, 648)])
# polygon_id: p373
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p373)
p374 = pya.Polygon([pya.Point(168, 108), pya.Point(168, 432), pya.Point(264, 432), pya.Point(264, 108)])
# polygon_id: p374
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p374)
p375 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 972), pya.Point(480, 972), pya.Point(480, 648)])
# polygon_id: p375
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p375)
p376 = pya.Polygon([pya.Point(384, 108), pya.Point(384, 432), pya.Point(480, 432), pya.Point(480, 108)])
# polygon_id: p376
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p376)
p377 = pya.Polygon([pya.Point(600, 648), pya.Point(600, 972), pya.Point(696, 972), pya.Point(696, 648)])
# polygon_id: p377
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p377)
p378 = pya.Polygon([pya.Point(600, 108), pya.Point(600, 432), pya.Point(696, 432), pya.Point(696, 108)])
# polygon_id: p378
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p378)
p379 = pya.Polygon([pya.Point(816, 648), pya.Point(816, 972), pya.Point(912, 972), pya.Point(912, 648)])
# polygon_id: p379
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p379)
p380 = pya.Polygon([pya.Point(816, 108), pya.Point(816, 432), pya.Point(912, 432), pya.Point(912, 108)])
# polygon_id: p380
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p380)
p381 = pya.Polygon([pya.Point(1032, 648), pya.Point(1032, 972), pya.Point(1128, 972), pya.Point(1128, 648)])
# polygon_id: p381
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p381)
p382 = pya.Polygon([pya.Point(1032, 108), pya.Point(1032, 432), pya.Point(1128, 432), pya.Point(1128, 108)])
# polygon_id: p382
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p382)
p383 = pya.Polygon([pya.Point(1248, 648), pya.Point(1248, 972), pya.Point(1344, 972), pya.Point(1344, 648)])
# polygon_id: p383
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p383)
p384 = pya.Polygon([pya.Point(1248, 108), pya.Point(1248, 432), pya.Point(1344, 432), pya.Point(1344, 108)])
# polygon_id: p384
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p384)
p385 = pya.Polygon([pya.Point(1464, 648), pya.Point(1464, 972), pya.Point(1560, 972), pya.Point(1560, 648)])
# polygon_id: p385
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p385)
p386 = pya.Polygon([pya.Point(1464, 108), pya.Point(1464, 432), pya.Point(1560, 432), pya.Point(1560, 108)])
# polygon_id: p386
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p386)
p387 = pya.Polygon([pya.Point(1680, 648), pya.Point(1680, 972), pya.Point(1776, 972), pya.Point(1776, 648)])
# polygon_id: p387
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p387)
p388 = pya.Polygon([pya.Point(1680, 108), pya.Point(1680, 432), pya.Point(1776, 432), pya.Point(1776, 108)])
# polygon_id: p388
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p388)
p389 = pya.Polygon([pya.Point(1896, 648), pya.Point(1896, 972), pya.Point(1992, 972), pya.Point(1992, 648)])
# polygon_id: p389
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p389)
p390 = pya.Polygon([pya.Point(1896, 108), pya.Point(1896, 432), pya.Point(1992, 432), pya.Point(1992, 108)])
# polygon_id: p390
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p390)
p391 = pya.Polygon([pya.Point(184, 648), pya.Point(184, 972), pya.Point(1976, 972), pya.Point(1976, 648)])
# polygon_id: p391
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p391)
p392 = pya.Polygon([pya.Point(184, 108), pya.Point(184, 432), pya.Point(1976, 432), pya.Point(1976, 108)])
# polygon_id: p392
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p392)
p393 = pya.Polygon([pya.Point(0, 1012), pya.Point(0, 1040), pya.Point(2160, 1040), pya.Point(2160, 1012)])
# polygon_id: p393
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p393)
p394 = pya.Polygon([pya.Point(0, 904), pya.Point(0, 932), pya.Point(2160, 932), pya.Point(2160, 904)])
# polygon_id: p394
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p394)
p395 = pya.Polygon([pya.Point(0, 796), pya.Point(0, 824), pya.Point(2160, 824), pya.Point(2160, 796)])
# polygon_id: p395
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p395)
p396 = pya.Polygon([pya.Point(0, 688), pya.Point(0, 716), pya.Point(2160, 716), pya.Point(2160, 688)])
# polygon_id: p396
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p396)
p397 = pya.Polygon([pya.Point(0, 580), pya.Point(0, 608), pya.Point(2160, 608), pya.Point(2160, 580)])
# polygon_id: p397
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p397)
p398 = pya.Polygon([pya.Point(0, 472), pya.Point(0, 500), pya.Point(2160, 500), pya.Point(2160, 472)])
# polygon_id: p398
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p398)
p399 = pya.Polygon([pya.Point(0, 364), pya.Point(0, 392), pya.Point(2160, 392), pya.Point(2160, 364)])
# polygon_id: p399
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p399)
p400 = pya.Polygon([pya.Point(0, 256), pya.Point(0, 284), pya.Point(2160, 284), pya.Point(2160, 256)])
# polygon_id: p400
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p400)
p401 = pya.Polygon([pya.Point(0, 148), pya.Point(0, 176), pya.Point(2160, 176), pya.Point(2160, 148)])
# polygon_id: p401
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p401)
p402 = pya.Polygon([pya.Point(0, 40), pya.Point(0, 68), pya.Point(2160, 68), pya.Point(2160, 40)])
# polygon_id: p402
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p402)
p403 = pya.Polygon([pya.Point(236, 492), pya.Point(236, 584), pya.Point(584, 584), pya.Point(584, 492)])
# polygon_id: p403
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p403)
p404 = pya.Polygon([pya.Point(712, 496), pya.Point(712, 584), pya.Point(1884, 584), pya.Point(1884, 496)])
# polygon_id: p404
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p404)
p405 = pya.Polygon([pya.Point(0, 1048), pya.Point(0, 1112), pya.Point(2160, 1112), pya.Point(2160, 1048)])
# polygon_id: p405
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p405)
p406 = pya.Polygon([pya.Point(0, -32), pya.Point(0, 32), pya.Point(2160, 32), pya.Point(2160, -32)])
# polygon_id: p406
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p406)
p407 = pya.Polygon([pya.Point(180, 1044), pya.Point(180, 1116), pya.Point(252, 1116), pya.Point(252, 1044)])
# polygon_id: p407
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p407)
p408 = pya.Polygon([pya.Point(180, -36), pya.Point(180, 36), pya.Point(252, 36), pya.Point(252, -36)])
# polygon_id: p408
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p408)
p409 = pya.Polygon([pya.Point(244, 504), pya.Point(244, 576), pya.Point(316, 576), pya.Point(316, 504)])
# polygon_id: p409
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p409)
p410 = pya.Polygon([pya.Point(396, 1044), pya.Point(396, 1116), pya.Point(468, 1116), pya.Point(468, 1044)])
# polygon_id: p410
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p410)
p411 = pya.Polygon([pya.Point(396, 900), pya.Point(396, 972), pya.Point(468, 972), pya.Point(468, 900)])
# polygon_id: p411
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p411)
p412 = pya.Polygon([pya.Point(396, 108), pya.Point(396, 180), pya.Point(468, 180), pya.Point(468, 108)])
# polygon_id: p412
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p412)
p413 = pya.Polygon([pya.Point(396, -36), pya.Point(396, 36), pya.Point(468, 36), pya.Point(468, -36)])
# polygon_id: p413
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p413)
p414 = pya.Polygon([pya.Point(612, 1044), pya.Point(612, 1116), pya.Point(684, 1116), pya.Point(684, 1044)])
# polygon_id: p414
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p414)
p415 = pya.Polygon([pya.Point(612, -36), pya.Point(612, 36), pya.Point(684, 36), pya.Point(684, -36)])
# polygon_id: p415
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p415)
p416 = pya.Polygon([pya.Point(720, 504), pya.Point(720, 576), pya.Point(792, 576), pya.Point(792, 504)])
# polygon_id: p416
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p416)
p417 = pya.Polygon([pya.Point(828, 1044), pya.Point(828, 1116), pya.Point(900, 1116), pya.Point(900, 1044)])
# polygon_id: p417
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p417)
p418 = pya.Polygon([pya.Point(828, 900), pya.Point(828, 972), pya.Point(900, 972), pya.Point(900, 900)])
# polygon_id: p418
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p418)
p419 = pya.Polygon([pya.Point(828, 108), pya.Point(828, 180), pya.Point(900, 180), pya.Point(900, 108)])
# polygon_id: p419
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p419)
p420 = pya.Polygon([pya.Point(828, -36), pya.Point(828, 36), pya.Point(900, 36), pya.Point(900, -36)])
# polygon_id: p420
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p420)
p421 = pya.Polygon([pya.Point(936, 504), pya.Point(936, 576), pya.Point(1008, 576), pya.Point(1008, 504)])
# polygon_id: p421
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p421)
p422 = pya.Polygon([pya.Point(1044, 1044), pya.Point(1044, 1116), pya.Point(1116, 1116), pya.Point(1116, 1044)])
# polygon_id: p422
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p422)
p423 = pya.Polygon([pya.Point(1044, -36), pya.Point(1044, 36), pya.Point(1116, 36), pya.Point(1116, -36)])
# polygon_id: p423
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p423)
p424 = pya.Polygon([pya.Point(1152, 504), pya.Point(1152, 576), pya.Point(1224, 576), pya.Point(1224, 504)])
# polygon_id: p424
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p424)
p425 = pya.Polygon([pya.Point(1260, 1044), pya.Point(1260, 1116), pya.Point(1332, 1116), pya.Point(1332, 1044)])
# polygon_id: p425
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p425)
p426 = pya.Polygon([pya.Point(1260, 900), pya.Point(1260, 972), pya.Point(1332, 972), pya.Point(1332, 900)])
# polygon_id: p426
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p426)
p427 = pya.Polygon([pya.Point(1260, 108), pya.Point(1260, 180), pya.Point(1332, 180), pya.Point(1332, 108)])
# polygon_id: p427
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p427)
p428 = pya.Polygon([pya.Point(1260, -36), pya.Point(1260, 36), pya.Point(1332, 36), pya.Point(1332, -36)])
# polygon_id: p428
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p428)
p429 = pya.Polygon([pya.Point(1368, 504), pya.Point(1368, 576), pya.Point(1440, 576), pya.Point(1440, 504)])
# polygon_id: p429
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p429)
p430 = pya.Polygon([pya.Point(1476, 1044), pya.Point(1476, 1116), pya.Point(1548, 1116), pya.Point(1548, 1044)])
# polygon_id: p430
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p430)
p431 = pya.Polygon([pya.Point(1476, -36), pya.Point(1476, 36), pya.Point(1548, 36), pya.Point(1548, -36)])
# polygon_id: p431
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p431)
p432 = pya.Polygon([pya.Point(1584, 504), pya.Point(1584, 576), pya.Point(1656, 576), pya.Point(1656, 504)])
# polygon_id: p432
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p432)
p433 = pya.Polygon([pya.Point(1692, 1044), pya.Point(1692, 1116), pya.Point(1764, 1116), pya.Point(1764, 1044)])
# polygon_id: p433
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p433)
p434 = pya.Polygon([pya.Point(1692, 900), pya.Point(1692, 972), pya.Point(1764, 972), pya.Point(1764, 900)])
# polygon_id: p434
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p434)
p435 = pya.Polygon([pya.Point(1692, 108), pya.Point(1692, 180), pya.Point(1764, 180), pya.Point(1764, 108)])
# polygon_id: p435
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p435)
p436 = pya.Polygon([pya.Point(1692, -36), pya.Point(1692, 36), pya.Point(1764, 36), pya.Point(1764, -36)])
# polygon_id: p436
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p436)
p437 = pya.Polygon([pya.Point(1800, 504), pya.Point(1800, 576), pya.Point(1872, 576), pya.Point(1872, 504)])
# polygon_id: p437
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p437)
p438 = pya.Polygon([pya.Point(1908, 1044), pya.Point(1908, 1116), pya.Point(1980, 1116), pya.Point(1980, 1044)])
# polygon_id: p438
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p438)
p439 = pya.Polygon([pya.Point(1908, -36), pya.Point(1908, 36), pya.Point(1980, 36), pya.Point(1980, -36)])
# polygon_id: p439
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p439)
p440 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 540), pya.Point(2160, 540), pya.Point(2160, 0)])
# polygon_id: p440
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(12, 0))).insert(p440)
p441 = pya.Polygon([pya.Point(0, 992), pya.Point(0, 1168), pya.Point(2160, 1168), pya.Point(2160, 992)])
# polygon_id: p441
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p441)
p442 = pya.Polygon([pya.Point(0, 452), pya.Point(0, 628), pya.Point(216, 628), pya.Point(216, 452)])
# polygon_id: p442
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p442)
p443 = pya.Polygon([pya.Point(1944, 452), pya.Point(1944, 628), pya.Point(2160, 628), pya.Point(2160, 452)])
# polygon_id: p443
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p443)
p444 = pya.Polygon([pya.Point(0, -88), pya.Point(0, 88), pya.Point(2160, 88), pya.Point(2160, -88)])
# polygon_id: p444
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p444)
p445 = pya.Polygon([pya.Point(716, -20), pya.Point(716, 1102), pya.Point(796, 1102), pya.Point(796, -20)])
# polygon_id: p445
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p445)
p446 = pya.Polygon([pya.Point(284, -20), pya.Point(284, 1102), pya.Point(364, 1102), pya.Point(364, -20)])
# polygon_id: p446
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p446)
p447 = pya.Polygon([pya.Point(932, -20), pya.Point(932, 1102), pya.Point(1012, 1102), pya.Point(1012, -20)])
# polygon_id: p447
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p447)
p448 = pya.Polygon([pya.Point(1796, -20), pya.Point(1796, 1102), pya.Point(1876, 1102), pya.Point(1876, -20)])
# polygon_id: p448
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p448)
p449 = pya.Polygon([pya.Point(1148, -20), pya.Point(1148, 1102), pya.Point(1228, 1102), pya.Point(1228, -20)])
# polygon_id: p449
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p449)
p450 = pya.Polygon([pya.Point(1364, -20), pya.Point(1364, 1102), pya.Point(1444, 1102), pya.Point(1444, -20)])
# polygon_id: p450
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p450)
p451 = pya.Polygon([pya.Point(1580, -20), pya.Point(1580, 1102), pya.Point(1660, 1102), pya.Point(1660, -20)])
# polygon_id: p451
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p451)
p452 = pya.Polygon([pya.Point(2012, -20), pya.Point(2012, 1102), pya.Point(2092, 1102), pya.Point(2092, -20)])
# polygon_id: p452
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p452)
p453 = pya.Polygon([pya.Point(68, -20), pya.Point(68, 1102), pya.Point(148, 1102), pya.Point(148, -20)])
# polygon_id: p453
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p453)
p454 = pya.Polygon([pya.Point(500, -20), pya.Point(500, 1102), pya.Point(580, 1102), pya.Point(580, -20)])
# polygon_id: p454
cell_BUFx6f_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p454)
p461 = pya.Polygon([pya.Point(580, 108), pya.Point(580, 180), pya.Point(936, 180), pya.Point(936, 900), pya.Point(580, 900), pya.Point(580, 972), pya.Point(1008, 972), pya.Point(1008, 108)])
# polygon_id: p461
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p461)
p462 = pya.Polygon([pya.Point(160, 108), pya.Point(160, 180), pya.Point(408, 180), pya.Point(408, 900), pya.Point(160, 900), pya.Point(160, 972), pya.Point(480, 972), pya.Point(480, 576), pya.Point(812, 576), pya.Point(812, 504), pya.Point(480, 504), pya.Point(480, 108)])
# polygon_id: p462
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p462)
p463 = pya.Polygon([pya.Point(72, 252), pya.Point(72, 828), pya.Point(220, 828), pya.Point(220, 756), pya.Point(144, 756), pya.Point(144, 576), pya.Point(292, 576), pya.Point(292, 504), pya.Point(144, 504), pya.Point(144, 324), pya.Point(220, 324), pya.Point(220, 252)])
# polygon_id: p463
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p463)
p464 = pya.Polygon([pya.Point(0, -36), pya.Point(0, 36), pya.Point(1080, 36), pya.Point(1080, -36)])
# polygon_id: p464
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p464)
p465 = pya.Polygon([pya.Point(0, 1044), pya.Point(0, 1116), pya.Point(1080, 1116), pya.Point(1080, 1044)])
# polygon_id: p465
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p465)
p466 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(1080, 1080), pya.Point(1080, 540)])
# polygon_id: p466
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(13, 0))).insert(p466)
p467 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(1080, 1080), pya.Point(1080, 540)])
# polygon_id: p467
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(1, 0))).insert(p467)
p468 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 1080), pya.Point(1080, 1080), pya.Point(1080, 0)])
# polygon_id: p468
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(100, 0))).insert(p468)
p469 = pya.Polygon([pya.Point(816, 0), pya.Point(816, 432), pya.Point(912, 432), pya.Point(912, 0)])
# polygon_id: p469
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p469)
p470 = pya.Polygon([pya.Point(816, 648), pya.Point(816, 1080), pya.Point(912, 1080), pya.Point(912, 648)])
# polygon_id: p470
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p470)
p471 = pya.Polygon([pya.Point(600, 108), pya.Point(600, 432), pya.Point(696, 432), pya.Point(696, 108)])
# polygon_id: p471
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p471)
p472 = pya.Polygon([pya.Point(600, 648), pya.Point(600, 972), pya.Point(696, 972), pya.Point(696, 648)])
# polygon_id: p472
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p472)
p473 = pya.Polygon([pya.Point(384, 0), pya.Point(384, 432), pya.Point(480, 432), pya.Point(480, 0)])
# polygon_id: p473
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p473)
p474 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 1080), pya.Point(480, 1080), pya.Point(480, 648)])
# polygon_id: p474
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p474)
p475 = pya.Polygon([pya.Point(168, 108), pya.Point(168, 432), pya.Point(264, 432), pya.Point(264, 108)])
# polygon_id: p475
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p475)
p476 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 972), pya.Point(264, 972), pya.Point(264, 648)])
# polygon_id: p476
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p476)
p477 = pya.Polygon([pya.Point(816, 108), pya.Point(816, 432), pya.Point(912, 432), pya.Point(912, 108)])
# polygon_id: p477
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p477)
p478 = pya.Polygon([pya.Point(816, 648), pya.Point(816, 972), pya.Point(912, 972), pya.Point(912, 648)])
# polygon_id: p478
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p478)
p479 = pya.Polygon([pya.Point(600, 108), pya.Point(600, 432), pya.Point(696, 432), pya.Point(696, 108)])
# polygon_id: p479
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p479)
p480 = pya.Polygon([pya.Point(600, 648), pya.Point(600, 972), pya.Point(696, 972), pya.Point(696, 648)])
# polygon_id: p480
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p480)
p481 = pya.Polygon([pya.Point(384, 108), pya.Point(384, 432), pya.Point(480, 432), pya.Point(480, 108)])
# polygon_id: p481
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p481)
p482 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 972), pya.Point(480, 972), pya.Point(480, 648)])
# polygon_id: p482
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p482)
p483 = pya.Polygon([pya.Point(168, 108), pya.Point(168, 432), pya.Point(264, 432), pya.Point(264, 108)])
# polygon_id: p483
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p483)
p484 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 972), pya.Point(264, 972), pya.Point(264, 648)])
# polygon_id: p484
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p484)
p485 = pya.Polygon([pya.Point(184, 108), pya.Point(184, 324), pya.Point(384, 324), pya.Point(384, 432), pya.Point(896, 432), pya.Point(896, 108)])
# polygon_id: p485
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p485)
p486 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 756), pya.Point(184, 756), pya.Point(184, 972), pya.Point(896, 972), pya.Point(896, 648)])
# polygon_id: p486
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p486)
p487 = pya.Polygon([pya.Point(0, 40), pya.Point(0, 68), pya.Point(1080, 68), pya.Point(1080, 40)])
# polygon_id: p487
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p487)
p488 = pya.Polygon([pya.Point(0, 148), pya.Point(0, 176), pya.Point(1080, 176), pya.Point(1080, 148)])
# polygon_id: p488
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p488)
p489 = pya.Polygon([pya.Point(0, 256), pya.Point(0, 284), pya.Point(1080, 284), pya.Point(1080, 256)])
# polygon_id: p489
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p489)
p490 = pya.Polygon([pya.Point(0, 364), pya.Point(0, 392), pya.Point(1080, 392), pya.Point(1080, 364)])
# polygon_id: p490
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p490)
p491 = pya.Polygon([pya.Point(0, 472), pya.Point(0, 500), pya.Point(1080, 500), pya.Point(1080, 472)])
# polygon_id: p491
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p491)
p492 = pya.Polygon([pya.Point(0, 580), pya.Point(0, 608), pya.Point(1080, 608), pya.Point(1080, 580)])
# polygon_id: p492
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p492)
p493 = pya.Polygon([pya.Point(0, 688), pya.Point(0, 716), pya.Point(1080, 716), pya.Point(1080, 688)])
# polygon_id: p493
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p493)
p494 = pya.Polygon([pya.Point(0, 796), pya.Point(0, 824), pya.Point(1080, 824), pya.Point(1080, 796)])
# polygon_id: p494
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p494)
p495 = pya.Polygon([pya.Point(0, 904), pya.Point(0, 932), pya.Point(1080, 932), pya.Point(1080, 904)])
# polygon_id: p495
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p495)
p496 = pya.Polygon([pya.Point(0, 1012), pya.Point(0, 1040), pya.Point(1080, 1040), pya.Point(1080, 1012)])
# polygon_id: p496
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p496)
p497 = pya.Polygon([pya.Point(0, -32), pya.Point(0, 32), pya.Point(1080, 32), pya.Point(1080, -32)])
# polygon_id: p497
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p497)
p498 = pya.Polygon([pya.Point(0, 1048), pya.Point(0, 1112), pya.Point(1080, 1112), pya.Point(1080, 1048)])
# polygon_id: p498
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p498)
p499 = pya.Polygon([pya.Point(496, 496), pya.Point(496, 584), pya.Point(584, 584), pya.Point(584, 496)])
# polygon_id: p499
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p499)
p500 = pya.Polygon([pya.Point(712, 496), pya.Point(712, 584), pya.Point(800, 584), pya.Point(800, 496)])
# polygon_id: p500
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p500)
p501 = pya.Polygon([pya.Point(216, 496), pya.Point(216, 584), pya.Point(368, 584), pya.Point(368, 496)])
# polygon_id: p501
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p501)
p502 = pya.Polygon([pya.Point(828, -36), pya.Point(828, 36), pya.Point(900, 36), pya.Point(900, -36)])
# polygon_id: p502
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p502)
p503 = pya.Polygon([pya.Point(828, 1044), pya.Point(828, 1116), pya.Point(900, 1116), pya.Point(900, 1044)])
# polygon_id: p503
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p503)
p504 = pya.Polygon([pya.Point(612, -36), pya.Point(612, 36), pya.Point(684, 36), pya.Point(684, -36)])
# polygon_id: p504
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p504)
p505 = pya.Polygon([pya.Point(612, 108), pya.Point(612, 180), pya.Point(684, 180), pya.Point(684, 108)])
# polygon_id: p505
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p505)
p506 = pya.Polygon([pya.Point(612, 900), pya.Point(612, 972), pya.Point(684, 972), pya.Point(684, 900)])
# polygon_id: p506
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p506)
p507 = pya.Polygon([pya.Point(612, 1044), pya.Point(612, 1116), pya.Point(684, 1116), pya.Point(684, 1044)])
# polygon_id: p507
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p507)
p508 = pya.Polygon([pya.Point(504, 504), pya.Point(504, 576), pya.Point(576, 576), pya.Point(576, 504)])
# polygon_id: p508
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p508)
p509 = pya.Polygon([pya.Point(396, -36), pya.Point(396, 36), pya.Point(468, 36), pya.Point(468, -36)])
# polygon_id: p509
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p509)
p510 = pya.Polygon([pya.Point(720, 504), pya.Point(720, 576), pya.Point(792, 576), pya.Point(792, 504)])
# polygon_id: p510
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p510)
p511 = pya.Polygon([pya.Point(396, 1044), pya.Point(396, 1116), pya.Point(468, 1116), pya.Point(468, 1044)])
# polygon_id: p511
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p511)
p512 = pya.Polygon([pya.Point(220, 504), pya.Point(220, 576), pya.Point(292, 576), pya.Point(292, 504)])
# polygon_id: p512
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p512)
p513 = pya.Polygon([pya.Point(180, -36), pya.Point(180, 36), pya.Point(252, 36), pya.Point(252, -36)])
# polygon_id: p513
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p513)
p514 = pya.Polygon([pya.Point(180, 108), pya.Point(180, 180), pya.Point(252, 180), pya.Point(252, 108)])
# polygon_id: p514
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p514)
p515 = pya.Polygon([pya.Point(180, 900), pya.Point(180, 972), pya.Point(252, 972), pya.Point(252, 900)])
# polygon_id: p515
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p515)
p516 = pya.Polygon([pya.Point(180, 1044), pya.Point(180, 1116), pya.Point(252, 1116), pya.Point(252, 1044)])
# polygon_id: p516
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p516)
p517 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 540), pya.Point(1080, 540), pya.Point(1080, 0)])
# polygon_id: p517
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(12, 0))).insert(p517)
p518 = pya.Polygon([pya.Point(864, 452), pya.Point(864, 628), pya.Point(1080, 628), pya.Point(1080, 452)])
# polygon_id: p518
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p518)
p519 = pya.Polygon([pya.Point(0, -88), pya.Point(0, 88), pya.Point(1080, 88), pya.Point(1080, -88)])
# polygon_id: p519
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p519)
p520 = pya.Polygon([pya.Point(0, 992), pya.Point(0, 1168), pya.Point(1080, 1168), pya.Point(1080, 992)])
# polygon_id: p520
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p520)
p521 = pya.Polygon([pya.Point(0, 452), pya.Point(0, 628), pya.Point(216, 628), pya.Point(216, 452)])
# polygon_id: p521
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p521)
p522 = pya.Polygon([pya.Point(932, -20), pya.Point(932, 1102), pya.Point(1012, 1102), pya.Point(1012, -20)])
# polygon_id: p522
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p522)
p523 = pya.Polygon([pya.Point(716, -20), pya.Point(716, 1102), pya.Point(796, 1102), pya.Point(796, -20)])
# polygon_id: p523
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p523)
p524 = pya.Polygon([pya.Point(500, -20), pya.Point(500, 1102), pya.Point(580, 1102), pya.Point(580, -20)])
# polygon_id: p524
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p524)
p525 = pya.Polygon([pya.Point(284, -20), pya.Point(284, 1102), pya.Point(364, 1102), pya.Point(364, -20)])
# polygon_id: p525
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p525)
p526 = pya.Polygon([pya.Point(68, -20), pya.Point(68, 1102), pya.Point(148, 1102), pya.Point(148, -20)])
# polygon_id: p526
cell_BUFx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p526)
p533 = pya.Polygon([pya.Point(512, 288), pya.Point(512, 360), pya.Point(2172, 360), pya.Point(2172, 288)])
# polygon_id: p533
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p533)
p534 = pya.Polygon([pya.Point(916, 432), pya.Point(916, 504), pya.Point(2348, 504), pya.Point(2348, 432)])
# polygon_id: p534
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p534)
p535 = pya.Polygon([pya.Point(668, 576), pya.Point(668, 648), pya.Point(2756, 648), pya.Point(2756, 576)])
# polygon_id: p535
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p535)
p536 = pya.Polygon([pya.Point(236, 720), pya.Point(236, 792), pya.Point(2508, 792), pya.Point(2508, 720)])
# polygon_id: p536
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p536)
p537 = pya.Polygon([pya.Point(916, 432), pya.Point(916, 504), pya.Point(2348, 504), pya.Point(2348, 432)])
# polygon_id: p537
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p537)
p538 = pya.Polygon([pya.Point(2060, 288), pya.Point(2060, 360), pya.Point(2172, 360), pya.Point(2172, 288)])
# polygon_id: p538
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p538)
p539 = pya.Polygon([pya.Point(2016, 360), pya.Point(2016, 432), pya.Point(2132, 432), pya.Point(2132, 360)])
# polygon_id: p539
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p539)
p540 = pya.Polygon([pya.Point(1908, 736), pya.Point(1908, 972), pya.Point(1980, 972), pya.Point(1980, 736)])
# polygon_id: p540
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p540)
p541 = pya.Polygon([pya.Point(1296, 900), pya.Point(1296, 972), pya.Point(1980, 972), pya.Point(1980, 900)])
# polygon_id: p541
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p541)
p542 = pya.Polygon([pya.Point(496, 288), pya.Point(496, 360), pya.Point(1128, 360), pya.Point(1128, 288)])
# polygon_id: p542
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p542)
p543 = pya.Polygon([pya.Point(1296, 108), pya.Point(1296, 180), pya.Point(1980, 180), pya.Point(1980, 108)])
# polygon_id: p543
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p543)
p544 = pya.Polygon([pya.Point(2104, 108), pya.Point(2104, 180), pya.Point(2648, 180), pya.Point(2648, 108)])
# polygon_id: p544
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p544)
p545 = pya.Polygon([pya.Point(2664, 484), pya.Point(2664, 668), pya.Point(2736, 668), pya.Point(2736, 484)])
# polygon_id: p545
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p545)
p546 = pya.Polygon([pya.Point(2448, 484), pya.Point(2448, 792), pya.Point(2520, 792), pya.Point(2520, 484)])
# polygon_id: p546
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p546)
p547 = pya.Polygon([pya.Point(2396, 720), pya.Point(2396, 792), pya.Point(2520, 792), pya.Point(2520, 720)])
# polygon_id: p547
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p547)
p548 = pya.Polygon([pya.Point(2232, 432), pya.Point(2232, 504), pya.Point(2348, 504), pya.Point(2348, 432)])
# polygon_id: p548
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p548)
p549 = pya.Polygon([pya.Point(2232, 432), pya.Point(2232, 596), pya.Point(2304, 596), pya.Point(2304, 432)])
# polygon_id: p549
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p549)
p550 = pya.Polygon([pya.Point(2104, 900), pya.Point(2104, 972), pya.Point(2648, 972), pya.Point(2648, 900)])
# polygon_id: p550
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p550)
p551 = pya.Polygon([pya.Point(1296, 108), pya.Point(1296, 972), pya.Point(1368, 972), pya.Point(1368, 108)])
# polygon_id: p551
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p551)
p552 = pya.Polygon([pya.Point(1800, 412), pya.Point(1800, 596), pya.Point(1872, 596), pya.Point(1872, 412)])
# polygon_id: p552
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p552)
p553 = pya.Polygon([pya.Point(904, 432), pya.Point(904, 504), pya.Point(1052, 504), pya.Point(1052, 432)])
# polygon_id: p553
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p553)
p554 = pya.Polygon([pya.Point(1584, 484), pya.Point(1584, 792), pya.Point(1656, 792), pya.Point(1656, 484)])
# polygon_id: p554
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p554)
p555 = pya.Polygon([pya.Point(1532, 720), pya.Point(1532, 792), pya.Point(1656, 792), pya.Point(1656, 720)])
# polygon_id: p555
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p555)
p556 = pya.Polygon([pya.Point(1908, 108), pya.Point(1908, 272), pya.Point(1980, 272), pya.Point(1980, 108)])
# polygon_id: p556
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p556)
p557 = pya.Polygon([pya.Point(496, 288), pya.Point(496, 828), pya.Point(568, 828), pya.Point(568, 288)])
# polygon_id: p557
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p557)
p558 = pya.Polygon([pya.Point(236, 720), pya.Point(236, 792), pya.Point(360, 792), pya.Point(360, 720)])
# polygon_id: p558
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p558)
p559 = pya.Polygon([pya.Point(668, 576), pya.Point(668, 648), pya.Point(792, 648), pya.Point(792, 576)])
# polygon_id: p559
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p559)
p560 = pya.Polygon([pya.Point(496, 756), pya.Point(496, 828), pya.Point(920, 828), pya.Point(920, 756)])
# polygon_id: p560
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p560)
p561 = pya.Polygon([pya.Point(160, 108), pya.Point(160, 180), pya.Point(1136, 180), pya.Point(1136, 108)])
# polygon_id: p561
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p561)
p562 = pya.Polygon([pya.Point(2016, 360), pya.Point(2016, 596), pya.Point(2088, 596), pya.Point(2088, 360)])
# polygon_id: p562
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p562)
p563 = pya.Polygon([pya.Point(288, 484), pya.Point(288, 792), pya.Point(360, 792), pya.Point(360, 484)])
# polygon_id: p563
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p563)
p564 = pya.Polygon([pya.Point(720, 484), pya.Point(720, 648), pya.Point(792, 648), pya.Point(792, 484)])
# polygon_id: p564
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p564)
p565 = pya.Polygon([pya.Point(160, 900), pya.Point(160, 972), pya.Point(1136, 972), pya.Point(1136, 900)])
# polygon_id: p565
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p565)
p566 = pya.Polygon([pya.Point(936, 432), pya.Point(936, 596), pya.Point(1008, 596), pya.Point(1008, 432)])
# polygon_id: p566
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p566)
p567 = pya.Polygon([pya.Point(1152, 484), pya.Point(1152, 668), pya.Point(1224, 668), pya.Point(1224, 484)])
# polygon_id: p567
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p567)
p568 = pya.Polygon([pya.Point(0, 1044), pya.Point(0, 1116), pya.Point(3024, 1116), pya.Point(3024, 1044)])
# polygon_id: p568
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p568)
p569 = pya.Polygon([pya.Point(0, -36), pya.Point(0, 36), pya.Point(3024, 36), pya.Point(3024, -36)])
# polygon_id: p569
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p569)
p570 = pya.Polygon([pya.Point(2080, 288), pya.Point(2080, 360), pya.Point(2152, 360), pya.Point(2152, 288)])
# polygon_id: p570
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p570)
p571 = pya.Polygon([pya.Point(532, 288), pya.Point(532, 360), pya.Point(604, 360), pya.Point(604, 288)])
# polygon_id: p571
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p571)
p572 = pya.Polygon([pya.Point(2664, 576), pya.Point(2664, 648), pya.Point(2736, 648), pya.Point(2736, 576)])
# polygon_id: p572
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p572)
p573 = pya.Polygon([pya.Point(2416, 720), pya.Point(2416, 792), pya.Point(2488, 792), pya.Point(2488, 720)])
# polygon_id: p573
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p573)
p574 = pya.Polygon([pya.Point(2256, 432), pya.Point(2256, 504), pya.Point(2328, 504), pya.Point(2328, 432)])
# polygon_id: p574
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p574)
p575 = pya.Polygon([pya.Point(1800, 432), pya.Point(1800, 504), pya.Point(1872, 504), pya.Point(1872, 432)])
# polygon_id: p575
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p575)
p576 = pya.Polygon([pya.Point(936, 432), pya.Point(936, 504), pya.Point(1008, 504), pya.Point(1008, 432)])
# polygon_id: p576
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p576)
p577 = pya.Polygon([pya.Point(1152, 576), pya.Point(1152, 648), pya.Point(1224, 648), pya.Point(1224, 576)])
# polygon_id: p577
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p577)
p578 = pya.Polygon([pya.Point(1552, 720), pya.Point(1552, 792), pya.Point(1624, 792), pya.Point(1624, 720)])
# polygon_id: p578
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p578)
p579 = pya.Polygon([pya.Point(256, 720), pya.Point(256, 792), pya.Point(328, 792), pya.Point(328, 720)])
# polygon_id: p579
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p579)
p580 = pya.Polygon([pya.Point(688, 576), pya.Point(688, 648), pya.Point(760, 648), pya.Point(760, 576)])
# polygon_id: p580
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(21, 0))).insert(p580)
p581 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(3024, 1080), pya.Point(3024, 540)])
# polygon_id: p581
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(13, 0))).insert(p581)
p582 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(3024, 1080), pya.Point(3024, 540)])
# polygon_id: p582
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(1, 0))).insert(p582)
p583 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 1080), pya.Point(3024, 1080), pya.Point(3024, 0)])
# polygon_id: p583
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(100, 0))).insert(p583)
p584 = pya.Polygon([pya.Point(2760, 0), pya.Point(2760, 432), pya.Point(2856, 432), pya.Point(2856, 0)])
# polygon_id: p584
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p584)
p585 = pya.Polygon([pya.Point(2760, 648), pya.Point(2760, 1080), pya.Point(2856, 1080), pya.Point(2856, 648)])
# polygon_id: p585
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p585)
p586 = pya.Polygon([pya.Point(2544, 108), pya.Point(2544, 432), pya.Point(2640, 432), pya.Point(2640, 108)])
# polygon_id: p586
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p586)
p587 = pya.Polygon([pya.Point(2544, 648), pya.Point(2544, 972), pya.Point(2640, 972), pya.Point(2640, 648)])
# polygon_id: p587
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p587)
p588 = pya.Polygon([pya.Point(2328, 0), pya.Point(2328, 432), pya.Point(2424, 432), pya.Point(2424, 0)])
# polygon_id: p588
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p588)
p589 = pya.Polygon([pya.Point(2328, 648), pya.Point(2328, 1080), pya.Point(2424, 1080), pya.Point(2424, 648)])
# polygon_id: p589
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p589)
p590 = pya.Polygon([pya.Point(2112, 108), pya.Point(2112, 432), pya.Point(2208, 432), pya.Point(2208, 108)])
# polygon_id: p590
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p590)
p591 = pya.Polygon([pya.Point(2112, 648), pya.Point(2112, 972), pya.Point(2208, 972), pya.Point(2208, 648)])
# polygon_id: p591
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p591)
p592 = pya.Polygon([pya.Point(1896, 108), pya.Point(1896, 432), pya.Point(1992, 432), pya.Point(1992, 108)])
# polygon_id: p592
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p592)
p593 = pya.Polygon([pya.Point(1896, 648), pya.Point(1896, 972), pya.Point(1992, 972), pya.Point(1992, 648)])
# polygon_id: p593
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p593)
p594 = pya.Polygon([pya.Point(1248, 0), pya.Point(1248, 432), pya.Point(1344, 432), pya.Point(1344, 0)])
# polygon_id: p594
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p594)
p595 = pya.Polygon([pya.Point(1248, 648), pya.Point(1248, 1080), pya.Point(1344, 1080), pya.Point(1344, 648)])
# polygon_id: p595
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p595)
p596 = pya.Polygon([pya.Point(1032, 108), pya.Point(1032, 432), pya.Point(1128, 432), pya.Point(1128, 108)])
# polygon_id: p596
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p596)
p597 = pya.Polygon([pya.Point(1032, 648), pya.Point(1032, 972), pya.Point(1128, 972), pya.Point(1128, 648)])
# polygon_id: p597
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p597)
p598 = pya.Polygon([pya.Point(816, 108), pya.Point(816, 432), pya.Point(912, 432), pya.Point(912, 108)])
# polygon_id: p598
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p598)
p599 = pya.Polygon([pya.Point(816, 648), pya.Point(816, 972), pya.Point(912, 972), pya.Point(912, 648)])
# polygon_id: p599
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p599)
p600 = pya.Polygon([pya.Point(384, 0), pya.Point(384, 432), pya.Point(480, 432), pya.Point(480, 0)])
# polygon_id: p600
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p600)
p601 = pya.Polygon([pya.Point(168, 108), pya.Point(168, 432), pya.Point(264, 432), pya.Point(264, 108)])
# polygon_id: p601
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p601)
p602 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 1080), pya.Point(480, 1080), pya.Point(480, 648)])
# polygon_id: p602
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p602)
p603 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 972), pya.Point(264, 972), pya.Point(264, 648)])
# polygon_id: p603
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p603)
p604 = pya.Polygon([pya.Point(2760, 108), pya.Point(2760, 432), pya.Point(2856, 432), pya.Point(2856, 108)])
# polygon_id: p604
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p604)
p605 = pya.Polygon([pya.Point(2760, 648), pya.Point(2760, 972), pya.Point(2856, 972), pya.Point(2856, 648)])
# polygon_id: p605
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p605)
p606 = pya.Polygon([pya.Point(2544, 108), pya.Point(2544, 432), pya.Point(2640, 432), pya.Point(2640, 108)])
# polygon_id: p606
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p606)
p607 = pya.Polygon([pya.Point(2544, 648), pya.Point(2544, 972), pya.Point(2640, 972), pya.Point(2640, 648)])
# polygon_id: p607
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p607)
p608 = pya.Polygon([pya.Point(2328, 108), pya.Point(2328, 432), pya.Point(2424, 432), pya.Point(2424, 108)])
# polygon_id: p608
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p608)
p609 = pya.Polygon([pya.Point(2328, 648), pya.Point(2328, 972), pya.Point(2424, 972), pya.Point(2424, 648)])
# polygon_id: p609
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p609)
p610 = pya.Polygon([pya.Point(2112, 108), pya.Point(2112, 432), pya.Point(2208, 432), pya.Point(2208, 108)])
# polygon_id: p610
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p610)
p611 = pya.Polygon([pya.Point(2112, 648), pya.Point(2112, 972), pya.Point(2208, 972), pya.Point(2208, 648)])
# polygon_id: p611
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p611)
p612 = pya.Polygon([pya.Point(1896, 108), pya.Point(1896, 432), pya.Point(1992, 432), pya.Point(1992, 108)])
# polygon_id: p612
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p612)
p613 = pya.Polygon([pya.Point(1896, 648), pya.Point(1896, 972), pya.Point(1992, 972), pya.Point(1992, 648)])
# polygon_id: p613
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p613)
p614 = pya.Polygon([pya.Point(1248, 108), pya.Point(1248, 432), pya.Point(1344, 432), pya.Point(1344, 108)])
# polygon_id: p614
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p614)
p615 = pya.Polygon([pya.Point(1248, 648), pya.Point(1248, 972), pya.Point(1344, 972), pya.Point(1344, 648)])
# polygon_id: p615
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p615)
p616 = pya.Polygon([pya.Point(1032, 108), pya.Point(1032, 432), pya.Point(1128, 432), pya.Point(1128, 108)])
# polygon_id: p616
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p616)
p617 = pya.Polygon([pya.Point(1032, 648), pya.Point(1032, 972), pya.Point(1128, 972), pya.Point(1128, 648)])
# polygon_id: p617
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p617)
p618 = pya.Polygon([pya.Point(816, 648), pya.Point(816, 972), pya.Point(912, 972), pya.Point(912, 648)])
# polygon_id: p618
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p618)
p619 = pya.Polygon([pya.Point(816, 108), pya.Point(816, 432), pya.Point(912, 432), pya.Point(912, 108)])
# polygon_id: p619
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p619)
p620 = pya.Polygon([pya.Point(384, 108), pya.Point(384, 432), pya.Point(480, 432), pya.Point(480, 108)])
# polygon_id: p620
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p620)
p621 = pya.Polygon([pya.Point(168, 108), pya.Point(168, 432), pya.Point(264, 432), pya.Point(264, 108)])
# polygon_id: p621
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p621)
p622 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 972), pya.Point(264, 972), pya.Point(264, 648)])
# polygon_id: p622
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p622)
p623 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 972), pya.Point(480, 972), pya.Point(480, 648)])
# polygon_id: p623
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p623)
p624 = pya.Polygon([pya.Point(184, 108), pya.Point(184, 432), pya.Point(2840, 432), pya.Point(2840, 108)])
# polygon_id: p624
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p624)
p625 = pya.Polygon([pya.Point(184, 648), pya.Point(184, 972), pya.Point(2840, 972), pya.Point(2840, 648)])
# polygon_id: p625
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p625)
p626 = pya.Polygon([pya.Point(0, 1012), pya.Point(0, 1040), pya.Point(3024, 1040), pya.Point(3024, 1012)])
# polygon_id: p626
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p626)
p627 = pya.Polygon([pya.Point(0, 904), pya.Point(0, 932), pya.Point(3024, 932), pya.Point(3024, 904)])
# polygon_id: p627
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p627)
p628 = pya.Polygon([pya.Point(0, 796), pya.Point(0, 824), pya.Point(3024, 824), pya.Point(3024, 796)])
# polygon_id: p628
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p628)
p629 = pya.Polygon([pya.Point(0, 688), pya.Point(0, 716), pya.Point(3024, 716), pya.Point(3024, 688)])
# polygon_id: p629
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p629)
p630 = pya.Polygon([pya.Point(0, 580), pya.Point(0, 608), pya.Point(3024, 608), pya.Point(3024, 580)])
# polygon_id: p630
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p630)
p631 = pya.Polygon([pya.Point(0, 472), pya.Point(0, 500), pya.Point(3024, 500), pya.Point(3024, 472)])
# polygon_id: p631
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p631)
p632 = pya.Polygon([pya.Point(0, 364), pya.Point(0, 392), pya.Point(3024, 392), pya.Point(3024, 364)])
# polygon_id: p632
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p632)
p633 = pya.Polygon([pya.Point(0, 256), pya.Point(0, 284), pya.Point(3024, 284), pya.Point(3024, 256)])
# polygon_id: p633
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p633)
p634 = pya.Polygon([pya.Point(0, 148), pya.Point(0, 176), pya.Point(3024, 176), pya.Point(3024, 148)])
# polygon_id: p634
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p634)
p635 = pya.Polygon([pya.Point(0, 40), pya.Point(0, 68), pya.Point(3024, 68), pya.Point(3024, 40)])
# polygon_id: p635
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p635)
p636 = pya.Polygon([pya.Point(2656, 496), pya.Point(2656, 584), pya.Point(2744, 584), pya.Point(2744, 496)])
# polygon_id: p636
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p636)
p637 = pya.Polygon([pya.Point(2440, 496), pya.Point(2440, 584), pya.Point(2528, 584), pya.Point(2528, 496)])
# polygon_id: p637
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p637)
p638 = pya.Polygon([pya.Point(2008, 496), pya.Point(2008, 584), pya.Point(2096, 584), pya.Point(2096, 496)])
# polygon_id: p638
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p638)
p639 = pya.Polygon([pya.Point(2224, 496), pya.Point(2224, 584), pya.Point(2312, 584), pya.Point(2312, 496)])
# polygon_id: p639
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p639)
p640 = pya.Polygon([pya.Point(1792, 496), pya.Point(1792, 584), pya.Point(1880, 584), pya.Point(1880, 496)])
# polygon_id: p640
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p640)
p641 = pya.Polygon([pya.Point(1576, 496), pya.Point(1576, 584), pya.Point(1664, 584), pya.Point(1664, 496)])
# polygon_id: p641
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p641)
p642 = pya.Polygon([pya.Point(1144, 496), pya.Point(1144, 584), pya.Point(1448, 584), pya.Point(1448, 496)])
# polygon_id: p642
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p642)
p643 = pya.Polygon([pya.Point(928, 496), pya.Point(928, 584), pya.Point(1016, 584), pya.Point(1016, 496)])
# polygon_id: p643
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p643)
p644 = pya.Polygon([pya.Point(712, 496), pya.Point(712, 584), pya.Point(800, 584), pya.Point(800, 496)])
# polygon_id: p644
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p644)
p645 = pya.Polygon([pya.Point(280, 496), pya.Point(280, 584), pya.Point(584, 584), pya.Point(584, 496)])
# polygon_id: p645
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p645)
p646 = pya.Polygon([pya.Point(0, 1048), pya.Point(0, 1112), pya.Point(3024, 1112), pya.Point(3024, 1048)])
# polygon_id: p646
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p646)
p647 = pya.Polygon([pya.Point(0, -32), pya.Point(0, 32), pya.Point(3024, 32), pya.Point(3024, -32)])
# polygon_id: p647
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p647)
p648 = pya.Polygon([pya.Point(2448, 504), pya.Point(2448, 576), pya.Point(2520, 576), pya.Point(2520, 504)])
# polygon_id: p648
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p648)
p649 = pya.Polygon([pya.Point(2232, 504), pya.Point(2232, 576), pya.Point(2304, 576), pya.Point(2304, 504)])
# polygon_id: p649
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p649)
p650 = pya.Polygon([pya.Point(2664, 504), pya.Point(2664, 576), pya.Point(2736, 576), pya.Point(2736, 504)])
# polygon_id: p650
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p650)
p651 = pya.Polygon([pya.Point(2448, 504), pya.Point(2448, 576), pya.Point(2520, 576), pya.Point(2520, 504)])
# polygon_id: p651
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p651)
p652 = pya.Polygon([pya.Point(2232, 504), pya.Point(2232, 576), pya.Point(2304, 576), pya.Point(2304, 504)])
# polygon_id: p652
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p652)
p653 = pya.Polygon([pya.Point(1800, 504), pya.Point(1800, 576), pya.Point(1872, 576), pya.Point(1872, 504)])
# polygon_id: p653
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p653)
p654 = pya.Polygon([pya.Point(1584, 504), pya.Point(1584, 576), pya.Point(1656, 576), pya.Point(1656, 504)])
# polygon_id: p654
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p654)
p655 = pya.Polygon([pya.Point(2664, 504), pya.Point(2664, 576), pya.Point(2736, 576), pya.Point(2736, 504)])
# polygon_id: p655
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p655)
p656 = pya.Polygon([pya.Point(2448, 504), pya.Point(2448, 576), pya.Point(2520, 576), pya.Point(2520, 504)])
# polygon_id: p656
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p656)
p657 = pya.Polygon([pya.Point(2232, 504), pya.Point(2232, 576), pya.Point(2304, 576), pya.Point(2304, 504)])
# polygon_id: p657
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p657)
p658 = pya.Polygon([pya.Point(2016, 504), pya.Point(2016, 576), pya.Point(2088, 576), pya.Point(2088, 504)])
# polygon_id: p658
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p658)
p659 = pya.Polygon([pya.Point(1800, 504), pya.Point(1800, 576), pya.Point(1872, 576), pya.Point(1872, 504)])
# polygon_id: p659
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p659)
p660 = pya.Polygon([pya.Point(1584, 504), pya.Point(1584, 576), pya.Point(1656, 576), pya.Point(1656, 504)])
# polygon_id: p660
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p660)
p661 = pya.Polygon([pya.Point(1152, 504), pya.Point(1152, 576), pya.Point(1224, 576), pya.Point(1224, 504)])
# polygon_id: p661
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p661)
p662 = pya.Polygon([pya.Point(936, 504), pya.Point(936, 576), pya.Point(1008, 576), pya.Point(1008, 504)])
# polygon_id: p662
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p662)
p663 = pya.Polygon([pya.Point(720, 504), pya.Point(720, 576), pya.Point(792, 576), pya.Point(792, 504)])
# polygon_id: p663
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p663)
p664 = pya.Polygon([pya.Point(288, 504), pya.Point(288, 576), pya.Point(360, 576), pya.Point(360, 504)])
# polygon_id: p664
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p664)
p665 = pya.Polygon([pya.Point(1476, 1044), pya.Point(1476, 1116), pya.Point(1548, 1116), pya.Point(1548, 1044)])
# polygon_id: p665
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p665)
p666 = pya.Polygon([pya.Point(1476, -36), pya.Point(1476, 36), pya.Point(1548, 36), pya.Point(1548, -36)])
# polygon_id: p666
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p666)
p667 = pya.Polygon([pya.Point(2124, 900), pya.Point(2124, 972), pya.Point(2196, 972), pya.Point(2196, 900)])
# polygon_id: p667
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p667)
p668 = pya.Polygon([pya.Point(2772, 1044), pya.Point(2772, 1116), pya.Point(2844, 1116), pya.Point(2844, 1044)])
# polygon_id: p668
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p668)
p669 = pya.Polygon([pya.Point(2772, 1044), pya.Point(2772, 1116), pya.Point(2844, 1116), pya.Point(2844, 1044)])
# polygon_id: p669
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p669)
p670 = pya.Polygon([pya.Point(2556, 1044), pya.Point(2556, 1116), pya.Point(2628, 1116), pya.Point(2628, 1044)])
# polygon_id: p670
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p670)
p671 = pya.Polygon([pya.Point(2556, 1044), pya.Point(2556, 1116), pya.Point(2628, 1116), pya.Point(2628, 1044)])
# polygon_id: p671
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p671)
p672 = pya.Polygon([pya.Point(2340, 1044), pya.Point(2340, 1116), pya.Point(2412, 1116), pya.Point(2412, 1044)])
# polygon_id: p672
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p672)
p673 = pya.Polygon([pya.Point(2340, 1044), pya.Point(2340, 1116), pya.Point(2412, 1116), pya.Point(2412, 1044)])
# polygon_id: p673
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p673)
p674 = pya.Polygon([pya.Point(2124, 1044), pya.Point(2124, 1116), pya.Point(2196, 1116), pya.Point(2196, 1044)])
# polygon_id: p674
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p674)
p675 = pya.Polygon([pya.Point(2124, 1044), pya.Point(2124, 1116), pya.Point(2196, 1116), pya.Point(2196, 1044)])
# polygon_id: p675
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p675)
p676 = pya.Polygon([pya.Point(1908, 1044), pya.Point(1908, 1116), pya.Point(1980, 1116), pya.Point(1980, 1044)])
# polygon_id: p676
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p676)
p677 = pya.Polygon([pya.Point(1908, 1044), pya.Point(1908, 1116), pya.Point(1980, 1116), pya.Point(1980, 1044)])
# polygon_id: p677
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p677)
p678 = pya.Polygon([pya.Point(2556, 900), pya.Point(2556, 972), pya.Point(2628, 972), pya.Point(2628, 900)])
# polygon_id: p678
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p678)
p679 = pya.Polygon([pya.Point(1908, 756), pya.Point(1908, 828), pya.Point(1980, 828), pya.Point(1980, 756)])
# polygon_id: p679
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p679)
p680 = pya.Polygon([pya.Point(1692, 1044), pya.Point(1692, 1116), pya.Point(1764, 1116), pya.Point(1764, 1044)])
# polygon_id: p680
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p680)
p681 = pya.Polygon([pya.Point(1908, 1044), pya.Point(1908, 1116), pya.Point(1980, 1116), pya.Point(1980, 1044)])
# polygon_id: p681
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p681)
p682 = pya.Polygon([pya.Point(2124, 1044), pya.Point(2124, 1116), pya.Point(2196, 1116), pya.Point(2196, 1044)])
# polygon_id: p682
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p682)
p683 = pya.Polygon([pya.Point(2340, 1044), pya.Point(2340, 1116), pya.Point(2412, 1116), pya.Point(2412, 1044)])
# polygon_id: p683
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p683)
p684 = pya.Polygon([pya.Point(2556, 1044), pya.Point(2556, 1116), pya.Point(2628, 1116), pya.Point(2628, 1044)])
# polygon_id: p684
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p684)
p685 = pya.Polygon([pya.Point(2772, 1044), pya.Point(2772, 1116), pya.Point(2844, 1116), pya.Point(2844, 1044)])
# polygon_id: p685
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p685)
p686 = pya.Polygon([pya.Point(180, 1044), pya.Point(180, 1116), pya.Point(252, 1116), pya.Point(252, 1044)])
# polygon_id: p686
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p686)
p687 = pya.Polygon([pya.Point(1044, 1044), pya.Point(1044, 1116), pya.Point(1116, 1116), pya.Point(1116, 1044)])
# polygon_id: p687
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p687)
p688 = pya.Polygon([pya.Point(396, 1044), pya.Point(396, 1116), pya.Point(468, 1116), pya.Point(468, 1044)])
# polygon_id: p688
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p688)
p689 = pya.Polygon([pya.Point(1044, 1044), pya.Point(1044, 1116), pya.Point(1116, 1116), pya.Point(1116, 1044)])
# polygon_id: p689
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p689)
p690 = pya.Polygon([pya.Point(612, 1044), pya.Point(612, 1116), pya.Point(684, 1116), pya.Point(684, 1044)])
# polygon_id: p690
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p690)
p691 = pya.Polygon([pya.Point(828, 1044), pya.Point(828, 1116), pya.Point(900, 1116), pya.Point(900, 1044)])
# polygon_id: p691
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p691)
p692 = pya.Polygon([pya.Point(1044, 1044), pya.Point(1044, 1116), pya.Point(1116, 1116), pya.Point(1116, 1044)])
# polygon_id: p692
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p692)
p693 = pya.Polygon([pya.Point(1260, 1044), pya.Point(1260, 1116), pya.Point(1332, 1116), pya.Point(1332, 1044)])
# polygon_id: p693
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p693)
p694 = pya.Polygon([pya.Point(828, 1044), pya.Point(828, 1116), pya.Point(900, 1116), pya.Point(900, 1044)])
# polygon_id: p694
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p694)
p695 = pya.Polygon([pya.Point(180, 1044), pya.Point(180, 1116), pya.Point(252, 1116), pya.Point(252, 1044)])
# polygon_id: p695
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p695)
p696 = pya.Polygon([pya.Point(180, 900), pya.Point(180, 972), pya.Point(252, 972), pya.Point(252, 900)])
# polygon_id: p696
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p696)
p697 = pya.Polygon([pya.Point(1044, 900), pya.Point(1044, 972), pya.Point(1116, 972), pya.Point(1116, 900)])
# polygon_id: p697
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p697)
p698 = pya.Polygon([pya.Point(828, 1044), pya.Point(828, 1116), pya.Point(900, 1116), pya.Point(900, 1044)])
# polygon_id: p698
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p698)
p699 = pya.Polygon([pya.Point(180, 1044), pya.Point(180, 1116), pya.Point(252, 1116), pya.Point(252, 1044)])
# polygon_id: p699
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p699)
p700 = pya.Polygon([pya.Point(828, 756), pya.Point(828, 828), pya.Point(900, 828), pya.Point(900, 756)])
# polygon_id: p700
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p700)
p701 = pya.Polygon([pya.Point(612, 1044), pya.Point(612, 1116), pya.Point(684, 1116), pya.Point(684, 1044)])
# polygon_id: p701
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p701)
p702 = pya.Polygon([pya.Point(1260, 1044), pya.Point(1260, 1116), pya.Point(1332, 1116), pya.Point(1332, 1044)])
# polygon_id: p702
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p702)
p703 = pya.Polygon([pya.Point(1260, 1044), pya.Point(1260, 1116), pya.Point(1332, 1116), pya.Point(1332, 1044)])
# polygon_id: p703
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p703)
p704 = pya.Polygon([pya.Point(396, 1044), pya.Point(396, 1116), pya.Point(468, 1116), pya.Point(468, 1044)])
# polygon_id: p704
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p704)
p705 = pya.Polygon([pya.Point(180, 1044), pya.Point(180, 1116), pya.Point(252, 1116), pya.Point(252, 1044)])
# polygon_id: p705
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p705)
p706 = pya.Polygon([pya.Point(1044, -36), pya.Point(1044, 36), pya.Point(1116, 36), pya.Point(1116, -36)])
# polygon_id: p706
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p706)
p707 = pya.Polygon([pya.Point(180, -36), pya.Point(180, 36), pya.Point(252, 36), pya.Point(252, -36)])
# polygon_id: p707
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p707)
p708 = pya.Polygon([pya.Point(828, 288), pya.Point(828, 360), pya.Point(900, 360), pya.Point(900, 288)])
# polygon_id: p708
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p708)
p709 = pya.Polygon([pya.Point(1260, -36), pya.Point(1260, 36), pya.Point(1332, 36), pya.Point(1332, -36)])
# polygon_id: p709
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p709)
p710 = pya.Polygon([pya.Point(1044, 108), pya.Point(1044, 180), pya.Point(1116, 180), pya.Point(1116, 108)])
# polygon_id: p710
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p710)
p711 = pya.Polygon([pya.Point(1260, -36), pya.Point(1260, 36), pya.Point(1332, 36), pya.Point(1332, -36)])
# polygon_id: p711
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p711)
p712 = pya.Polygon([pya.Point(396, -36), pya.Point(396, 36), pya.Point(468, 36), pya.Point(468, -36)])
# polygon_id: p712
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p712)
p713 = pya.Polygon([pya.Point(1044, -36), pya.Point(1044, 36), pya.Point(1116, 36), pya.Point(1116, -36)])
# polygon_id: p713
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p713)
p714 = pya.Polygon([pya.Point(828, -36), pya.Point(828, 36), pya.Point(900, 36), pya.Point(900, -36)])
# polygon_id: p714
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p714)
p715 = pya.Polygon([pya.Point(828, -36), pya.Point(828, 36), pya.Point(900, 36), pya.Point(900, -36)])
# polygon_id: p715
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p715)
p716 = pya.Polygon([pya.Point(1260, -36), pya.Point(1260, 36), pya.Point(1332, 36), pya.Point(1332, -36)])
# polygon_id: p716
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p716)
p717 = pya.Polygon([pya.Point(828, -36), pya.Point(828, 36), pya.Point(900, 36), pya.Point(900, -36)])
# polygon_id: p717
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p717)
p718 = pya.Polygon([pya.Point(612, -36), pya.Point(612, 36), pya.Point(684, 36), pya.Point(684, -36)])
# polygon_id: p718
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p718)
p719 = pya.Polygon([pya.Point(1044, -36), pya.Point(1044, 36), pya.Point(1116, 36), pya.Point(1116, -36)])
# polygon_id: p719
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p719)
p720 = pya.Polygon([pya.Point(1260, -36), pya.Point(1260, 36), pya.Point(1332, 36), pya.Point(1332, -36)])
# polygon_id: p720
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p720)
p721 = pya.Polygon([pya.Point(1044, -36), pya.Point(1044, 36), pya.Point(1116, 36), pya.Point(1116, -36)])
# polygon_id: p721
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p721)
p722 = pya.Polygon([pya.Point(396, -36), pya.Point(396, 36), pya.Point(468, 36), pya.Point(468, -36)])
# polygon_id: p722
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p722)
p723 = pya.Polygon([pya.Point(396, -36), pya.Point(396, 36), pya.Point(468, 36), pya.Point(468, -36)])
# polygon_id: p723
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p723)
p724 = pya.Polygon([pya.Point(180, -36), pya.Point(180, 36), pya.Point(252, 36), pya.Point(252, -36)])
# polygon_id: p724
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p724)
p725 = pya.Polygon([pya.Point(180, -36), pya.Point(180, 36), pya.Point(252, 36), pya.Point(252, -36)])
# polygon_id: p725
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p725)
p726 = pya.Polygon([pya.Point(828, -36), pya.Point(828, 36), pya.Point(900, 36), pya.Point(900, -36)])
# polygon_id: p726
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p726)
p727 = pya.Polygon([pya.Point(180, 108), pya.Point(180, 180), pya.Point(252, 180), pya.Point(252, 108)])
# polygon_id: p727
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p727)
p728 = pya.Polygon([pya.Point(2340, -36), pya.Point(2340, 36), pya.Point(2412, 36), pya.Point(2412, -36)])
# polygon_id: p728
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p728)
p729 = pya.Polygon([pya.Point(2340, -36), pya.Point(2340, 36), pya.Point(2412, 36), pya.Point(2412, -36)])
# polygon_id: p729
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p729)
p730 = pya.Polygon([pya.Point(2340, -36), pya.Point(2340, 36), pya.Point(2412, 36), pya.Point(2412, -36)])
# polygon_id: p730
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p730)
p731 = pya.Polygon([pya.Point(2772, -36), pya.Point(2772, 36), pya.Point(2844, 36), pya.Point(2844, -36)])
# polygon_id: p731
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p731)
p732 = pya.Polygon([pya.Point(1692, -36), pya.Point(1692, 36), pya.Point(1764, 36), pya.Point(1764, -36)])
# polygon_id: p732
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p732)
p733 = pya.Polygon([pya.Point(2772, -36), pya.Point(2772, 36), pya.Point(2844, 36), pya.Point(2844, -36)])
# polygon_id: p733
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p733)
p734 = pya.Polygon([pya.Point(2124, -36), pya.Point(2124, 36), pya.Point(2196, 36), pya.Point(2196, -36)])
# polygon_id: p734
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p734)
p735 = pya.Polygon([pya.Point(2124, -36), pya.Point(2124, 36), pya.Point(2196, 36), pya.Point(2196, -36)])
# polygon_id: p735
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p735)
p736 = pya.Polygon([pya.Point(2124, -36), pya.Point(2124, 36), pya.Point(2196, 36), pya.Point(2196, -36)])
# polygon_id: p736
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p736)
p737 = pya.Polygon([pya.Point(1908, -36), pya.Point(1908, 36), pya.Point(1980, 36), pya.Point(1980, -36)])
# polygon_id: p737
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p737)
p738 = pya.Polygon([pya.Point(1908, 180), pya.Point(1908, 252), pya.Point(1980, 252), pya.Point(1980, 180)])
# polygon_id: p738
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p738)
p739 = pya.Polygon([pya.Point(2124, -36), pya.Point(2124, 36), pya.Point(2196, 36), pya.Point(2196, -36)])
# polygon_id: p739
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p739)
p740 = pya.Polygon([pya.Point(2556, 108), pya.Point(2556, 180), pya.Point(2628, 180), pya.Point(2628, 108)])
# polygon_id: p740
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p740)
p741 = pya.Polygon([pya.Point(2340, -36), pya.Point(2340, 36), pya.Point(2412, 36), pya.Point(2412, -36)])
# polygon_id: p741
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p741)
p742 = pya.Polygon([pya.Point(1908, -36), pya.Point(1908, 36), pya.Point(1980, 36), pya.Point(1980, -36)])
# polygon_id: p742
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p742)
p743 = pya.Polygon([pya.Point(2556, -36), pya.Point(2556, 36), pya.Point(2628, 36), pya.Point(2628, -36)])
# polygon_id: p743
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p743)
p744 = pya.Polygon([pya.Point(1908, -36), pya.Point(1908, 36), pya.Point(1980, 36), pya.Point(1980, -36)])
# polygon_id: p744
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p744)
p745 = pya.Polygon([pya.Point(2772, -36), pya.Point(2772, 36), pya.Point(2844, 36), pya.Point(2844, -36)])
# polygon_id: p745
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p745)
p746 = pya.Polygon([pya.Point(1908, -36), pya.Point(1908, 36), pya.Point(1980, 36), pya.Point(1980, -36)])
# polygon_id: p746
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p746)
p747 = pya.Polygon([pya.Point(2556, -36), pya.Point(2556, 36), pya.Point(2628, 36), pya.Point(2628, -36)])
# polygon_id: p747
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p747)
p748 = pya.Polygon([pya.Point(2556, -36), pya.Point(2556, 36), pya.Point(2628, 36), pya.Point(2628, -36)])
# polygon_id: p748
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p748)
p749 = pya.Polygon([pya.Point(2556, -36), pya.Point(2556, 36), pya.Point(2628, 36), pya.Point(2628, -36)])
# polygon_id: p749
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p749)
p750 = pya.Polygon([pya.Point(2124, 108), pya.Point(2124, 180), pya.Point(2196, 180), pya.Point(2196, 108)])
# polygon_id: p750
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p750)
p751 = pya.Polygon([pya.Point(2772, -36), pya.Point(2772, 36), pya.Point(2844, 36), pya.Point(2844, -36)])
# polygon_id: p751
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p751)
p752 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 540), pya.Point(3024, 540), pya.Point(3024, 0)])
# polygon_id: p752
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(12, 0))).insert(p752)
p753 = pya.Polygon([pya.Point(0, 452), pya.Point(0, 628), pya.Point(216, 628), pya.Point(216, 452)])
# polygon_id: p753
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p753)
p754 = pya.Polygon([pya.Point(2808, 452), pya.Point(2808, 628), pya.Point(3024, 628), pya.Point(3024, 452)])
# polygon_id: p754
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p754)
p755 = pya.Polygon([pya.Point(0, -88), pya.Point(0, 88), pya.Point(3024, 88), pya.Point(3024, -88)])
# polygon_id: p755
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p755)
p756 = pya.Polygon([pya.Point(0, 992), pya.Point(0, 1168), pya.Point(3024, 1168), pya.Point(3024, 992)])
# polygon_id: p756
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p756)
p757 = pya.Polygon([pya.Point(68, -14), pya.Point(68, 1094), pya.Point(148, 1094), pya.Point(148, -14)])
# polygon_id: p757
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p757)
p758 = pya.Polygon([pya.Point(284, -14), pya.Point(284, 1094), pya.Point(364, 1094), pya.Point(364, -14)])
# polygon_id: p758
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p758)
p759 = pya.Polygon([pya.Point(500, -14), pya.Point(500, 1094), pya.Point(580, 1094), pya.Point(580, -14)])
# polygon_id: p759
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p759)
p760 = pya.Polygon([pya.Point(716, -14), pya.Point(716, 1094), pya.Point(796, 1094), pya.Point(796, -14)])
# polygon_id: p760
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p760)
p761 = pya.Polygon([pya.Point(932, -14), pya.Point(932, 1094), pya.Point(1012, 1094), pya.Point(1012, -14)])
# polygon_id: p761
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p761)
p762 = pya.Polygon([pya.Point(1148, -14), pya.Point(1148, 1094), pya.Point(1228, 1094), pya.Point(1228, -14)])
# polygon_id: p762
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p762)
p763 = pya.Polygon([pya.Point(1364, -14), pya.Point(1364, 1094), pya.Point(1444, 1094), pya.Point(1444, -14)])
# polygon_id: p763
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p763)
p764 = pya.Polygon([pya.Point(1580, -14), pya.Point(1580, 1094), pya.Point(1660, 1094), pya.Point(1660, -14)])
# polygon_id: p764
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p764)
p765 = pya.Polygon([pya.Point(1796, -14), pya.Point(1796, 1094), pya.Point(1876, 1094), pya.Point(1876, -14)])
# polygon_id: p765
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p765)
p766 = pya.Polygon([pya.Point(2012, -14), pya.Point(2012, 1094), pya.Point(2092, 1094), pya.Point(2092, -14)])
# polygon_id: p766
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p766)
p767 = pya.Polygon([pya.Point(2228, -14), pya.Point(2228, 1094), pya.Point(2308, 1094), pya.Point(2308, -14)])
# polygon_id: p767
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p767)
p768 = pya.Polygon([pya.Point(2444, -14), pya.Point(2444, 1094), pya.Point(2524, 1094), pya.Point(2524, -14)])
# polygon_id: p768
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p768)
p769 = pya.Polygon([pya.Point(2660, -14), pya.Point(2660, 1094), pya.Point(2740, 1094), pya.Point(2740, -14)])
# polygon_id: p769
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p769)
p770 = pya.Polygon([pya.Point(2876, -14), pya.Point(2876, 1094), pya.Point(2956, 1094), pya.Point(2956, -14)])
# polygon_id: p770
cell_FAx1_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p770)
p780 = pya.Polygon([pya.Point(72, 108), pya.Point(72, 972), pya.Point(220, 972), pya.Point(220, 900), pya.Point(144, 900), pya.Point(144, 576), pya.Point(312, 576), pya.Point(312, 504), pya.Point(144, 504), pya.Point(144, 180), pya.Point(220, 180), pya.Point(220, 108)])
# polygon_id: p780
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p780)
p781 = pya.Polygon([pya.Point(376, 108), pya.Point(376, 180), pya.Point(504, 180), pya.Point(504, 900), pya.Point(376, 900), pya.Point(376, 972), pya.Point(576, 972), pya.Point(576, 108)])
# polygon_id: p781
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p781)
p782 = pya.Polygon([pya.Point(0, 1044), pya.Point(0, 1116), pya.Point(864, 1116), pya.Point(864, 1044)])
# polygon_id: p782
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p782)
p783 = pya.Polygon([pya.Point(0, -36), pya.Point(0, 36), pya.Point(864, 36), pya.Point(864, -36)])
# polygon_id: p783
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p783)
p784 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(864, 1080), pya.Point(864, 540)])
# polygon_id: p784
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(13, 0))).insert(p784)
p785 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(864, 1080), pya.Point(864, 540)])
# polygon_id: p785
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(1, 0))).insert(p785)
p786 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 1080), pya.Point(864, 1080), pya.Point(864, 0)])
# polygon_id: p786
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(100, 0))).insert(p786)
p787 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 1080), pya.Point(264, 1080), pya.Point(264, 648)])
# polygon_id: p787
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p787)
p788 = pya.Polygon([pya.Point(168, 0), pya.Point(168, 432), pya.Point(264, 432), pya.Point(264, 0)])
# polygon_id: p788
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p788)
p789 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 972), pya.Point(480, 972), pya.Point(480, 648)])
# polygon_id: p789
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p789)
p790 = pya.Polygon([pya.Point(384, 108), pya.Point(384, 432), pya.Point(480, 432), pya.Point(480, 108)])
# polygon_id: p790
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p790)
p791 = pya.Polygon([pya.Point(600, 648), pya.Point(600, 1080), pya.Point(696, 1080), pya.Point(696, 648)])
# polygon_id: p791
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p791)
p792 = pya.Polygon([pya.Point(600, 0), pya.Point(600, 432), pya.Point(696, 432), pya.Point(696, 0)])
# polygon_id: p792
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p792)
p793 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 972), pya.Point(264, 972), pya.Point(264, 648)])
# polygon_id: p793
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p793)
p794 = pya.Polygon([pya.Point(168, 108), pya.Point(168, 432), pya.Point(264, 432), pya.Point(264, 108)])
# polygon_id: p794
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p794)
p795 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 972), pya.Point(480, 972), pya.Point(480, 648)])
# polygon_id: p795
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p795)
p796 = pya.Polygon([pya.Point(384, 108), pya.Point(384, 432), pya.Point(480, 432), pya.Point(480, 108)])
# polygon_id: p796
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p796)
p797 = pya.Polygon([pya.Point(600, 648), pya.Point(600, 972), pya.Point(696, 972), pya.Point(696, 648)])
# polygon_id: p797
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p797)
p798 = pya.Polygon([pya.Point(600, 108), pya.Point(600, 432), pya.Point(696, 432), pya.Point(696, 108)])
# polygon_id: p798
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p798)
p799 = pya.Polygon([pya.Point(184, 648), pya.Point(184, 972), pya.Point(680, 972), pya.Point(680, 648)])
# polygon_id: p799
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p799)
p800 = pya.Polygon([pya.Point(184, 108), pya.Point(184, 432), pya.Point(680, 432), pya.Point(680, 108)])
# polygon_id: p800
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p800)
p801 = pya.Polygon([pya.Point(0, 1012), pya.Point(0, 1040), pya.Point(864, 1040), pya.Point(864, 1012)])
# polygon_id: p801
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p801)
p802 = pya.Polygon([pya.Point(0, 904), pya.Point(0, 932), pya.Point(864, 932), pya.Point(864, 904)])
# polygon_id: p802
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p802)
p803 = pya.Polygon([pya.Point(0, 796), pya.Point(0, 824), pya.Point(864, 824), pya.Point(864, 796)])
# polygon_id: p803
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p803)
p804 = pya.Polygon([pya.Point(0, 688), pya.Point(0, 716), pya.Point(864, 716), pya.Point(864, 688)])
# polygon_id: p804
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p804)
p805 = pya.Polygon([pya.Point(0, 580), pya.Point(0, 608), pya.Point(864, 608), pya.Point(864, 580)])
# polygon_id: p805
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p805)
p806 = pya.Polygon([pya.Point(0, 472), pya.Point(0, 500), pya.Point(864, 500), pya.Point(864, 472)])
# polygon_id: p806
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p806)
p807 = pya.Polygon([pya.Point(0, 364), pya.Point(0, 392), pya.Point(864, 392), pya.Point(864, 364)])
# polygon_id: p807
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p807)
p808 = pya.Polygon([pya.Point(0, 256), pya.Point(0, 284), pya.Point(864, 284), pya.Point(864, 256)])
# polygon_id: p808
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p808)
p809 = pya.Polygon([pya.Point(0, 148), pya.Point(0, 176), pya.Point(864, 176), pya.Point(864, 148)])
# polygon_id: p809
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p809)
p810 = pya.Polygon([pya.Point(0, 40), pya.Point(0, 68), pya.Point(864, 68), pya.Point(864, 40)])
# polygon_id: p810
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p810)
p811 = pya.Polygon([pya.Point(216, 496), pya.Point(216, 584), pya.Point(588, 584), pya.Point(588, 496)])
# polygon_id: p811
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p811)
p812 = pya.Polygon([pya.Point(0, 1048), pya.Point(0, 1112), pya.Point(864, 1112), pya.Point(864, 1048)])
# polygon_id: p812
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p812)
p813 = pya.Polygon([pya.Point(0, -32), pya.Point(0, 32), pya.Point(864, 32), pya.Point(864, -32)])
# polygon_id: p813
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p813)
p814 = pya.Polygon([pya.Point(180, 1044), pya.Point(180, 1116), pya.Point(252, 1116), pya.Point(252, 1044)])
# polygon_id: p814
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p814)
p815 = pya.Polygon([pya.Point(180, -36), pya.Point(180, 36), pya.Point(252, 36), pya.Point(252, -36)])
# polygon_id: p815
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p815)
p816 = pya.Polygon([pya.Point(220, 504), pya.Point(220, 576), pya.Point(292, 576), pya.Point(292, 504)])
# polygon_id: p816
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p816)
p817 = pya.Polygon([pya.Point(396, 1044), pya.Point(396, 1116), pya.Point(468, 1116), pya.Point(468, 1044)])
# polygon_id: p817
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p817)
p818 = pya.Polygon([pya.Point(396, 900), pya.Point(396, 972), pya.Point(468, 972), pya.Point(468, 900)])
# polygon_id: p818
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p818)
p819 = pya.Polygon([pya.Point(396, 108), pya.Point(396, 180), pya.Point(468, 180), pya.Point(468, 108)])
# polygon_id: p819
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p819)
p820 = pya.Polygon([pya.Point(396, -36), pya.Point(396, 36), pya.Point(468, 36), pya.Point(468, -36)])
# polygon_id: p820
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p820)
p821 = pya.Polygon([pya.Point(612, 1044), pya.Point(612, 1116), pya.Point(684, 1116), pya.Point(684, 1044)])
# polygon_id: p821
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p821)
p822 = pya.Polygon([pya.Point(612, -36), pya.Point(612, 36), pya.Point(684, 36), pya.Point(684, -36)])
# polygon_id: p822
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p822)
p823 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 540), pya.Point(864, 540), pya.Point(864, 0)])
# polygon_id: p823
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(12, 0))).insert(p823)
p824 = pya.Polygon([pya.Point(0, 452), pya.Point(0, 628), pya.Point(216, 628), pya.Point(216, 452)])
# polygon_id: p824
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p824)
p825 = pya.Polygon([pya.Point(0, 992), pya.Point(0, 1168), pya.Point(864, 1168), pya.Point(864, 992)])
# polygon_id: p825
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p825)
p826 = pya.Polygon([pya.Point(648, 452), pya.Point(648, 628), pya.Point(864, 628), pya.Point(864, 452)])
# polygon_id: p826
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p826)
p827 = pya.Polygon([pya.Point(0, -88), pya.Point(0, 88), pya.Point(864, 88), pya.Point(864, -88)])
# polygon_id: p827
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p827)
p828 = pya.Polygon([pya.Point(68, -20), pya.Point(68, 1100), pya.Point(148, 1100), pya.Point(148, -20)])
# polygon_id: p828
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p828)
p829 = pya.Polygon([pya.Point(284, -20), pya.Point(284, 1100), pya.Point(364, 1100), pya.Point(364, -20)])
# polygon_id: p829
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p829)
p830 = pya.Polygon([pya.Point(500, -20), pya.Point(500, 1100), pya.Point(580, 1100), pya.Point(580, -20)])
# polygon_id: p830
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p830)
p831 = pya.Polygon([pya.Point(716, -20), pya.Point(716, 1100), pya.Point(796, 1100), pya.Point(796, -20)])
# polygon_id: p831
cell_INVx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p831)
p838 = pya.Polygon([pya.Point(72, 108), pya.Point(72, 972), pya.Point(220, 972), pya.Point(220, 900), pya.Point(144, 900), pya.Point(144, 576), pya.Point(312, 576), pya.Point(312, 504), pya.Point(144, 504), pya.Point(144, 180), pya.Point(220, 180), pya.Point(220, 108)])
# polygon_id: p838
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p838)
p839 = pya.Polygon([pya.Point(376, 108), pya.Point(376, 180), pya.Point(936, 180), pya.Point(936, 900), pya.Point(376, 900), pya.Point(376, 972), pya.Point(1008, 972), pya.Point(1008, 108)])
# polygon_id: p839
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p839)
p840 = pya.Polygon([pya.Point(0, 1044), pya.Point(0, 1116), pya.Point(1080, 1116), pya.Point(1080, 1044)])
# polygon_id: p840
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p840)
p841 = pya.Polygon([pya.Point(0, -36), pya.Point(0, 36), pya.Point(1080, 36), pya.Point(1080, -36)])
# polygon_id: p841
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p841)
p842 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(1080, 1080), pya.Point(1080, 540)])
# polygon_id: p842
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(13, 0))).insert(p842)
p843 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(1080, 1080), pya.Point(1080, 540)])
# polygon_id: p843
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(1, 0))).insert(p843)
p844 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 1080), pya.Point(1080, 1080), pya.Point(1080, 0)])
# polygon_id: p844
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(100, 0))).insert(p844)
p845 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 1080), pya.Point(264, 1080), pya.Point(264, 648)])
# polygon_id: p845
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p845)
p846 = pya.Polygon([pya.Point(168, 0), pya.Point(168, 432), pya.Point(264, 432), pya.Point(264, 0)])
# polygon_id: p846
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p846)
p847 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 972), pya.Point(480, 972), pya.Point(480, 648)])
# polygon_id: p847
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p847)
p848 = pya.Polygon([pya.Point(384, 108), pya.Point(384, 432), pya.Point(480, 432), pya.Point(480, 108)])
# polygon_id: p848
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p848)
p849 = pya.Polygon([pya.Point(600, 648), pya.Point(600, 1080), pya.Point(696, 1080), pya.Point(696, 648)])
# polygon_id: p849
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p849)
p850 = pya.Polygon([pya.Point(600, 0), pya.Point(600, 432), pya.Point(696, 432), pya.Point(696, 0)])
# polygon_id: p850
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p850)
p851 = pya.Polygon([pya.Point(816, 648), pya.Point(816, 972), pya.Point(912, 972), pya.Point(912, 648)])
# polygon_id: p851
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p851)
p852 = pya.Polygon([pya.Point(816, 108), pya.Point(816, 432), pya.Point(912, 432), pya.Point(912, 108)])
# polygon_id: p852
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p852)
p853 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 972), pya.Point(264, 972), pya.Point(264, 648)])
# polygon_id: p853
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p853)
p854 = pya.Polygon([pya.Point(168, 108), pya.Point(168, 432), pya.Point(264, 432), pya.Point(264, 108)])
# polygon_id: p854
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p854)
p855 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 972), pya.Point(480, 972), pya.Point(480, 648)])
# polygon_id: p855
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p855)
p856 = pya.Polygon([pya.Point(384, 108), pya.Point(384, 432), pya.Point(480, 432), pya.Point(480, 108)])
# polygon_id: p856
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p856)
p857 = pya.Polygon([pya.Point(600, 648), pya.Point(600, 972), pya.Point(696, 972), pya.Point(696, 648)])
# polygon_id: p857
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p857)
p858 = pya.Polygon([pya.Point(600, 108), pya.Point(600, 432), pya.Point(696, 432), pya.Point(696, 108)])
# polygon_id: p858
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p858)
p859 = pya.Polygon([pya.Point(816, 648), pya.Point(816, 972), pya.Point(912, 972), pya.Point(912, 648)])
# polygon_id: p859
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p859)
p860 = pya.Polygon([pya.Point(816, 108), pya.Point(816, 432), pya.Point(912, 432), pya.Point(912, 108)])
# polygon_id: p860
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p860)
p861 = pya.Polygon([pya.Point(184, 648), pya.Point(184, 972), pya.Point(896, 972), pya.Point(896, 648)])
# polygon_id: p861
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p861)
p862 = pya.Polygon([pya.Point(184, 108), pya.Point(184, 432), pya.Point(896, 432), pya.Point(896, 108)])
# polygon_id: p862
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p862)
p863 = pya.Polygon([pya.Point(0, 1012), pya.Point(0, 1040), pya.Point(1080, 1040), pya.Point(1080, 1012)])
# polygon_id: p863
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p863)
p864 = pya.Polygon([pya.Point(0, 904), pya.Point(0, 932), pya.Point(1080, 932), pya.Point(1080, 904)])
# polygon_id: p864
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p864)
p865 = pya.Polygon([pya.Point(0, 796), pya.Point(0, 824), pya.Point(1080, 824), pya.Point(1080, 796)])
# polygon_id: p865
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p865)
p866 = pya.Polygon([pya.Point(0, 688), pya.Point(0, 716), pya.Point(1080, 716), pya.Point(1080, 688)])
# polygon_id: p866
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p866)
p867 = pya.Polygon([pya.Point(0, 580), pya.Point(0, 608), pya.Point(1080, 608), pya.Point(1080, 580)])
# polygon_id: p867
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p867)
p868 = pya.Polygon([pya.Point(0, 472), pya.Point(0, 500), pya.Point(1080, 500), pya.Point(1080, 472)])
# polygon_id: p868
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p868)
p869 = pya.Polygon([pya.Point(0, 364), pya.Point(0, 392), pya.Point(1080, 392), pya.Point(1080, 364)])
# polygon_id: p869
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p869)
p870 = pya.Polygon([pya.Point(0, 256), pya.Point(0, 284), pya.Point(1080, 284), pya.Point(1080, 256)])
# polygon_id: p870
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p870)
p871 = pya.Polygon([pya.Point(0, 148), pya.Point(0, 176), pya.Point(1080, 176), pya.Point(1080, 148)])
# polygon_id: p871
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p871)
p872 = pya.Polygon([pya.Point(0, 40), pya.Point(0, 68), pya.Point(1080, 68), pya.Point(1080, 40)])
# polygon_id: p872
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p872)
p873 = pya.Polygon([pya.Point(216, 496), pya.Point(216, 584), pya.Point(804, 584), pya.Point(804, 496)])
# polygon_id: p873
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p873)
p874 = pya.Polygon([pya.Point(0, 1048), pya.Point(0, 1112), pya.Point(1080, 1112), pya.Point(1080, 1048)])
# polygon_id: p874
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p874)
p875 = pya.Polygon([pya.Point(0, -32), pya.Point(0, 32), pya.Point(1080, 32), pya.Point(1080, -32)])
# polygon_id: p875
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p875)
p876 = pya.Polygon([pya.Point(180, 1044), pya.Point(180, 1116), pya.Point(252, 1116), pya.Point(252, 1044)])
# polygon_id: p876
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p876)
p877 = pya.Polygon([pya.Point(180, -36), pya.Point(180, 36), pya.Point(252, 36), pya.Point(252, -36)])
# polygon_id: p877
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p877)
p878 = pya.Polygon([pya.Point(220, 504), pya.Point(220, 576), pya.Point(292, 576), pya.Point(292, 504)])
# polygon_id: p878
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p878)
p879 = pya.Polygon([pya.Point(396, 1044), pya.Point(396, 1116), pya.Point(468, 1116), pya.Point(468, 1044)])
# polygon_id: p879
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p879)
p880 = pya.Polygon([pya.Point(396, 900), pya.Point(396, 972), pya.Point(468, 972), pya.Point(468, 900)])
# polygon_id: p880
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p880)
p881 = pya.Polygon([pya.Point(396, 108), pya.Point(396, 180), pya.Point(468, 180), pya.Point(468, 108)])
# polygon_id: p881
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p881)
p882 = pya.Polygon([pya.Point(396, -36), pya.Point(396, 36), pya.Point(468, 36), pya.Point(468, -36)])
# polygon_id: p882
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p882)
p883 = pya.Polygon([pya.Point(612, 1044), pya.Point(612, 1116), pya.Point(684, 1116), pya.Point(684, 1044)])
# polygon_id: p883
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p883)
p884 = pya.Polygon([pya.Point(612, -36), pya.Point(612, 36), pya.Point(684, 36), pya.Point(684, -36)])
# polygon_id: p884
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p884)
p885 = pya.Polygon([pya.Point(828, 1044), pya.Point(828, 1116), pya.Point(900, 1116), pya.Point(900, 1044)])
# polygon_id: p885
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p885)
p886 = pya.Polygon([pya.Point(828, 900), pya.Point(828, 972), pya.Point(900, 972), pya.Point(900, 900)])
# polygon_id: p886
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p886)
p887 = pya.Polygon([pya.Point(828, 108), pya.Point(828, 180), pya.Point(900, 180), pya.Point(900, 108)])
# polygon_id: p887
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p887)
p888 = pya.Polygon([pya.Point(828, -36), pya.Point(828, 36), pya.Point(900, 36), pya.Point(900, -36)])
# polygon_id: p888
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p888)
p889 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 540), pya.Point(1080, 540), pya.Point(1080, 0)])
# polygon_id: p889
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(12, 0))).insert(p889)
p890 = pya.Polygon([pya.Point(864, 452), pya.Point(864, 628), pya.Point(1080, 628), pya.Point(1080, 452)])
# polygon_id: p890
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p890)
p891 = pya.Polygon([pya.Point(0, 452), pya.Point(0, 628), pya.Point(216, 628), pya.Point(216, 452)])
# polygon_id: p891
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p891)
p892 = pya.Polygon([pya.Point(0, 992), pya.Point(0, 1168), pya.Point(1080, 1168), pya.Point(1080, 992)])
# polygon_id: p892
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p892)
p893 = pya.Polygon([pya.Point(0, -88), pya.Point(0, 88), pya.Point(1080, 88), pya.Point(1080, -88)])
# polygon_id: p893
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p893)
p894 = pya.Polygon([pya.Point(68, -20), pya.Point(68, 1102), pya.Point(148, 1102), pya.Point(148, -20)])
# polygon_id: p894
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p894)
p895 = pya.Polygon([pya.Point(284, -20), pya.Point(284, 1102), pya.Point(364, 1102), pya.Point(364, -20)])
# polygon_id: p895
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p895)
p896 = pya.Polygon([pya.Point(500, -20), pya.Point(500, 1102), pya.Point(580, 1102), pya.Point(580, -20)])
# polygon_id: p896
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p896)
p897 = pya.Polygon([pya.Point(716, -20), pya.Point(716, 1102), pya.Point(796, 1102), pya.Point(796, -20)])
# polygon_id: p897
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p897)
p898 = pya.Polygon([pya.Point(932, -20), pya.Point(932, 1102), pya.Point(1012, 1102), pya.Point(1012, -20)])
# polygon_id: p898
cell_INVx3_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p898)
p905 = pya.Polygon([pya.Point(0, -36), pya.Point(0, 36), pya.Point(432, 36), pya.Point(432, -36)])
# polygon_id: p905
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p905)
p906 = pya.Polygon([pya.Point(0, 1044), pya.Point(0, 1116), pya.Point(432, 1116), pya.Point(432, 1044)])
# polygon_id: p906
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p906)
p907 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 540), pya.Point(432, 540), pya.Point(432, 0)])
# polygon_id: p907
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(13, 0))).insert(p907)
p908 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(432, 1080), pya.Point(432, 540)])
# polygon_id: p908
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(1, 0))).insert(p908)
p909 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 1080), pya.Point(432, 1080), pya.Point(432, 0)])
# polygon_id: p909
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(100, 0))).insert(p909)
p910 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 1080), pya.Point(264, 1080), pya.Point(264, 648)])
# polygon_id: p910
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p910)
p911 = pya.Polygon([pya.Point(168, 0), pya.Point(168, 432), pya.Point(264, 432), pya.Point(264, 0)])
# polygon_id: p911
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p911)
p912 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 972), pya.Point(264, 972), pya.Point(264, 648)])
# polygon_id: p912
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p912)
p913 = pya.Polygon([pya.Point(168, 108), pya.Point(168, 432), pya.Point(264, 432), pya.Point(264, 108)])
# polygon_id: p913
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p913)
p914 = pya.Polygon([pya.Point(184, 648), pya.Point(184, 972), pya.Point(248, 972), pya.Point(248, 648)])
# polygon_id: p914
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p914)
p915 = pya.Polygon([pya.Point(184, 108), pya.Point(184, 432), pya.Point(248, 432), pya.Point(248, 108)])
# polygon_id: p915
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p915)
p916 = pya.Polygon([pya.Point(0, 1012), pya.Point(0, 1040), pya.Point(432, 1040), pya.Point(432, 1012)])
# polygon_id: p916
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p916)
p917 = pya.Polygon([pya.Point(0, 904), pya.Point(0, 932), pya.Point(432, 932), pya.Point(432, 904)])
# polygon_id: p917
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p917)
p918 = pya.Polygon([pya.Point(0, 796), pya.Point(0, 824), pya.Point(432, 824), pya.Point(432, 796)])
# polygon_id: p918
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p918)
p919 = pya.Polygon([pya.Point(0, 688), pya.Point(0, 716), pya.Point(432, 716), pya.Point(432, 688)])
# polygon_id: p919
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p919)
p920 = pya.Polygon([pya.Point(0, 580), pya.Point(0, 608), pya.Point(432, 608), pya.Point(432, 580)])
# polygon_id: p920
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p920)
p921 = pya.Polygon([pya.Point(0, 472), pya.Point(0, 500), pya.Point(432, 500), pya.Point(432, 472)])
# polygon_id: p921
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p921)
p922 = pya.Polygon([pya.Point(0, 364), pya.Point(0, 392), pya.Point(432, 392), pya.Point(432, 364)])
# polygon_id: p922
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p922)
p923 = pya.Polygon([pya.Point(0, 256), pya.Point(0, 284), pya.Point(432, 284), pya.Point(432, 256)])
# polygon_id: p923
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p923)
p924 = pya.Polygon([pya.Point(0, 148), pya.Point(0, 176), pya.Point(432, 176), pya.Point(432, 148)])
# polygon_id: p924
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p924)
p925 = pya.Polygon([pya.Point(0, 40), pya.Point(0, 68), pya.Point(432, 68), pya.Point(432, 40)])
# polygon_id: p925
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p925)
p926 = pya.Polygon([pya.Point(0, 1048), pya.Point(0, 1112), pya.Point(432, 1112), pya.Point(432, 1048)])
# polygon_id: p926
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p926)
p927 = pya.Polygon([pya.Point(0, -32), pya.Point(0, 32), pya.Point(432, 32), pya.Point(432, -32)])
# polygon_id: p927
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p927)
p928 = pya.Polygon([pya.Point(180, 1044), pya.Point(180, 1116), pya.Point(252, 1116), pya.Point(252, 1044)])
# polygon_id: p928
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p928)
p929 = pya.Polygon([pya.Point(180, -36), pya.Point(180, 36), pya.Point(252, 36), pya.Point(252, -36)])
# polygon_id: p929
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p929)
p930 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(432, 1080), pya.Point(432, 540)])
# polygon_id: p930
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(12, 0))).insert(p930)
p931 = pya.Polygon([pya.Point(0, 452), pya.Point(0, 628), pya.Point(432, 628), pya.Point(432, 452)])
# polygon_id: p931
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p931)
p932 = pya.Polygon([pya.Point(0, -88), pya.Point(0, 88), pya.Point(432, 88), pya.Point(432, -88)])
# polygon_id: p932
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p932)
p933 = pya.Polygon([pya.Point(0, 992), pya.Point(0, 1168), pya.Point(432, 1168), pya.Point(432, 992)])
# polygon_id: p933
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p933)
p934 = pya.Polygon([pya.Point(68, -20), pya.Point(68, 1100), pya.Point(148, 1100), pya.Point(148, -20)])
# polygon_id: p934
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p934)
p935 = pya.Polygon([pya.Point(284, -20), pya.Point(284, 1100), pya.Point(364, 1100), pya.Point(364, -20)])
# polygon_id: p935
cell_TAPCELL_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p935)
p938 = pya.Polygon([pya.Point(504, 180), pya.Point(504, 600), pya.Point(576, 600), pya.Point(576, 252), pya.Point(1136, 252), pya.Point(1136, 180)])
# polygon_id: p938
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p938)
p939 = pya.Polygon([pya.Point(720, 484), pya.Point(720, 828), pya.Point(160, 828), pya.Point(160, 900), pya.Point(792, 900), pya.Point(792, 484)])
# polygon_id: p939
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p939)
p940 = pya.Polygon([pya.Point(0, -36), pya.Point(0, 36), pya.Point(1296, 36), pya.Point(1296, -36)])
# polygon_id: p940
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p940)
p941 = pya.Polygon([pya.Point(0, 1044), pya.Point(0, 1116), pya.Point(1296, 1116), pya.Point(1296, 1044)])
# polygon_id: p941
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p941)
p942 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(1296, 1080), pya.Point(1296, 540)])
# polygon_id: p942
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(13, 0))).insert(p942)
p943 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(1296, 1080), pya.Point(1296, 540)])
# polygon_id: p943
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(1, 0))).insert(p943)
p944 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 1080), pya.Point(1296, 1080), pya.Point(1296, 0)])
# polygon_id: p944
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(100, 0))).insert(p944)
p945 = pya.Polygon([pya.Point(1032, 108), pya.Point(1032, 432), pya.Point(1128, 432), pya.Point(1128, 108)])
# polygon_id: p945
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p945)
p946 = pya.Polygon([pya.Point(816, 0), pya.Point(816, 432), pya.Point(912, 432), pya.Point(912, 0)])
# polygon_id: p946
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p946)
p947 = pya.Polygon([pya.Point(600, 108), pya.Point(600, 432), pya.Point(696, 432), pya.Point(696, 108)])
# polygon_id: p947
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p947)
p948 = pya.Polygon([pya.Point(600, 648), pya.Point(600, 972), pya.Point(696, 972), pya.Point(696, 648)])
# polygon_id: p948
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p948)
p949 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 1080), pya.Point(480, 1080), pya.Point(480, 648)])
# polygon_id: p949
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p949)
p950 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 972), pya.Point(264, 972), pya.Point(264, 648)])
# polygon_id: p950
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(17, 0))).insert(p950)
p951 = pya.Polygon([pya.Point(1032, 108), pya.Point(1032, 432), pya.Point(1128, 432), pya.Point(1128, 108)])
# polygon_id: p951
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p951)
p952 = pya.Polygon([pya.Point(816, 108), pya.Point(816, 432), pya.Point(912, 432), pya.Point(912, 108)])
# polygon_id: p952
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p952)
p953 = pya.Polygon([pya.Point(600, 108), pya.Point(600, 432), pya.Point(696, 432), pya.Point(696, 108)])
# polygon_id: p953
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p953)
p954 = pya.Polygon([pya.Point(600, 648), pya.Point(600, 972), pya.Point(696, 972), pya.Point(696, 648)])
# polygon_id: p954
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p954)
p955 = pya.Polygon([pya.Point(384, 648), pya.Point(384, 972), pya.Point(480, 972), pya.Point(480, 648)])
# polygon_id: p955
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p955)
p956 = pya.Polygon([pya.Point(168, 648), pya.Point(168, 972), pya.Point(264, 972), pya.Point(264, 648)])
# polygon_id: p956
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(88, 0))).insert(p956)
p957 = pya.Polygon([pya.Point(616, 108), pya.Point(616, 432), pya.Point(1112, 432), pya.Point(1112, 108)])
# polygon_id: p957
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p957)
p958 = pya.Polygon([pya.Point(184, 648), pya.Point(184, 972), pya.Point(680, 972), pya.Point(680, 648)])
# polygon_id: p958
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(11, 0))).insert(p958)
p959 = pya.Polygon([pya.Point(0, 40), pya.Point(0, 68), pya.Point(1296, 68), pya.Point(1296, 40)])
# polygon_id: p959
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p959)
p960 = pya.Polygon([pya.Point(0, 148), pya.Point(0, 176), pya.Point(1296, 176), pya.Point(1296, 148)])
# polygon_id: p960
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p960)
p961 = pya.Polygon([pya.Point(0, 256), pya.Point(0, 284), pya.Point(1296, 284), pya.Point(1296, 256)])
# polygon_id: p961
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p961)
p962 = pya.Polygon([pya.Point(0, 364), pya.Point(0, 392), pya.Point(1296, 392), pya.Point(1296, 364)])
# polygon_id: p962
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p962)
p963 = pya.Polygon([pya.Point(0, 472), pya.Point(0, 500), pya.Point(1296, 500), pya.Point(1296, 472)])
# polygon_id: p963
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p963)
p964 = pya.Polygon([pya.Point(0, 580), pya.Point(0, 608), pya.Point(1296, 608), pya.Point(1296, 580)])
# polygon_id: p964
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p964)
p965 = pya.Polygon([pya.Point(0, 688), pya.Point(0, 716), pya.Point(1296, 716), pya.Point(1296, 688)])
# polygon_id: p965
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p965)
p966 = pya.Polygon([pya.Point(0, 796), pya.Point(0, 824), pya.Point(1296, 824), pya.Point(1296, 796)])
# polygon_id: p966
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p966)
p967 = pya.Polygon([pya.Point(0, 904), pya.Point(0, 932), pya.Point(1296, 932), pya.Point(1296, 904)])
# polygon_id: p967
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p967)
p968 = pya.Polygon([pya.Point(0, 1012), pya.Point(0, 1040), pya.Point(1296, 1040), pya.Point(1296, 1012)])
# polygon_id: p968
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p968)
p969 = pya.Polygon([pya.Point(0, -32), pya.Point(0, 32), pya.Point(1296, 32), pya.Point(1296, -32)])
# polygon_id: p969
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p969)
p970 = pya.Polygon([pya.Point(0, 1048), pya.Point(0, 1112), pya.Point(1296, 1112), pya.Point(1296, 1048)])
# polygon_id: p970
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p970)
p971 = pya.Polygon([pya.Point(712, 496), pya.Point(712, 584), pya.Point(1016, 584), pya.Point(1016, 496)])
# polygon_id: p971
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p971)
p972 = pya.Polygon([pya.Point(280, 496), pya.Point(280, 584), pya.Point(584, 584), pya.Point(584, 496)])
# polygon_id: p972
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p972)
p973 = pya.Polygon([pya.Point(1044, -36), pya.Point(1044, 36), pya.Point(1116, 36), pya.Point(1116, -36)])
# polygon_id: p973
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p973)
p974 = pya.Polygon([pya.Point(1044, 180), pya.Point(1044, 252), pya.Point(1116, 252), pya.Point(1116, 180)])
# polygon_id: p974
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p974)
p975 = pya.Polygon([pya.Point(1044, 1044), pya.Point(1044, 1116), pya.Point(1116, 1116), pya.Point(1116, 1044)])
# polygon_id: p975
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p975)
p976 = pya.Polygon([pya.Point(828, -36), pya.Point(828, 36), pya.Point(900, 36), pya.Point(900, -36)])
# polygon_id: p976
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p976)
p977 = pya.Polygon([pya.Point(828, 1044), pya.Point(828, 1116), pya.Point(900, 1116), pya.Point(900, 1044)])
# polygon_id: p977
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p977)
p978 = pya.Polygon([pya.Point(720, 504), pya.Point(720, 576), pya.Point(792, 576), pya.Point(792, 504)])
# polygon_id: p978
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p978)
p979 = pya.Polygon([pya.Point(612, -36), pya.Point(612, 36), pya.Point(684, 36), pya.Point(684, -36)])
# polygon_id: p979
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p979)
p980 = pya.Polygon([pya.Point(612, 180), pya.Point(612, 252), pya.Point(684, 252), pya.Point(684, 180)])
# polygon_id: p980
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p980)
p981 = pya.Polygon([pya.Point(612, 828), pya.Point(612, 900), pya.Point(684, 900), pya.Point(684, 828)])
# polygon_id: p981
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p981)
p982 = pya.Polygon([pya.Point(612, 1044), pya.Point(612, 1116), pya.Point(684, 1116), pya.Point(684, 1044)])
# polygon_id: p982
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p982)
p983 = pya.Polygon([pya.Point(504, 504), pya.Point(504, 576), pya.Point(576, 576), pya.Point(576, 504)])
# polygon_id: p983
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p983)
p984 = pya.Polygon([pya.Point(396, -36), pya.Point(396, 36), pya.Point(468, 36), pya.Point(468, -36)])
# polygon_id: p984
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p984)
p985 = pya.Polygon([pya.Point(396, 1044), pya.Point(396, 1116), pya.Point(468, 1116), pya.Point(468, 1044)])
# polygon_id: p985
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p985)
p986 = pya.Polygon([pya.Point(180, -36), pya.Point(180, 36), pya.Point(252, 36), pya.Point(252, -36)])
# polygon_id: p986
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p986)
p987 = pya.Polygon([pya.Point(180, 828), pya.Point(180, 900), pya.Point(252, 900), pya.Point(252, 828)])
# polygon_id: p987
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p987)
p988 = pya.Polygon([pya.Point(180, 1044), pya.Point(180, 1116), pya.Point(252, 1116), pya.Point(252, 1044)])
# polygon_id: p988
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p988)
p989 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 540), pya.Point(1296, 540), pya.Point(1296, 0)])
# polygon_id: p989
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(12, 0))).insert(p989)
p990 = pya.Polygon([pya.Point(0, -88), pya.Point(0, 88), pya.Point(1296, 88), pya.Point(1296, -88)])
# polygon_id: p990
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p990)
p991 = pya.Polygon([pya.Point(1080, 452), pya.Point(1080, 628), pya.Point(1296, 628), pya.Point(1296, 452)])
# polygon_id: p991
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p991)
p992 = pya.Polygon([pya.Point(0, 992), pya.Point(0, 1168), pya.Point(1296, 1168), pya.Point(1296, 992)])
# polygon_id: p992
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p992)
p993 = pya.Polygon([pya.Point(0, 452), pya.Point(0, 628), pya.Point(216, 628), pya.Point(216, 452)])
# polygon_id: p993
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p993)
p994 = pya.Polygon([pya.Point(1148, -20), pya.Point(1148, 1100), pya.Point(1228, 1100), pya.Point(1228, -20)])
# polygon_id: p994
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p994)
p995 = pya.Polygon([pya.Point(932, -20), pya.Point(932, 1100), pya.Point(1012, 1100), pya.Point(1012, -20)])
# polygon_id: p995
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p995)
p996 = pya.Polygon([pya.Point(716, -20), pya.Point(716, 1100), pya.Point(796, 1100), pya.Point(796, -20)])
# polygon_id: p996
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p996)
p997 = pya.Polygon([pya.Point(500, -20), pya.Point(500, 1100), pya.Point(580, 1100), pya.Point(580, -20)])
# polygon_id: p997
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p997)
p998 = pya.Polygon([pya.Point(284, -20), pya.Point(284, 1100), pya.Point(364, 1100), pya.Point(364, -20)])
# polygon_id: p998
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p998)
p999 = pya.Polygon([pya.Point(68, -20), pya.Point(68, 1100), pya.Point(148, 1100), pya.Point(148, -20)])
# polygon_id: p999
cell_DECAPx2_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p999)
p1004 = pya.Polygon([pya.Point(0, -36), pya.Point(0, 36), pya.Point(432, 36), pya.Point(432, -36)])
# polygon_id: p1004
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p1004)
p1005 = pya.Polygon([pya.Point(0, 1044), pya.Point(0, 1116), pya.Point(432, 1116), pya.Point(432, 1044)])
# polygon_id: p1005
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p1005)
p1006 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(432, 1080), pya.Point(432, 540)])
# polygon_id: p1006
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(13, 0))).insert(p1006)
p1007 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(432, 1080), pya.Point(432, 540)])
# polygon_id: p1007
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(1, 0))).insert(p1007)
p1008 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 1080), pya.Point(432, 1080), pya.Point(432, 0)])
# polygon_id: p1008
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(100, 0))).insert(p1008)
p1009 = pya.Polygon([pya.Point(0, 1012), pya.Point(0, 1040), pya.Point(432, 1040), pya.Point(432, 1012)])
# polygon_id: p1009
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1009)
p1010 = pya.Polygon([pya.Point(0, 904), pya.Point(0, 932), pya.Point(432, 932), pya.Point(432, 904)])
# polygon_id: p1010
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1010)
p1011 = pya.Polygon([pya.Point(0, 796), pya.Point(0, 824), pya.Point(432, 824), pya.Point(432, 796)])
# polygon_id: p1011
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1011)
p1012 = pya.Polygon([pya.Point(0, 688), pya.Point(0, 716), pya.Point(432, 716), pya.Point(432, 688)])
# polygon_id: p1012
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1012)
p1013 = pya.Polygon([pya.Point(0, 580), pya.Point(0, 608), pya.Point(432, 608), pya.Point(432, 580)])
# polygon_id: p1013
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1013)
p1014 = pya.Polygon([pya.Point(0, 472), pya.Point(0, 500), pya.Point(432, 500), pya.Point(432, 472)])
# polygon_id: p1014
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1014)
p1015 = pya.Polygon([pya.Point(0, 364), pya.Point(0, 392), pya.Point(432, 392), pya.Point(432, 364)])
# polygon_id: p1015
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1015)
p1016 = pya.Polygon([pya.Point(0, 256), pya.Point(0, 284), pya.Point(432, 284), pya.Point(432, 256)])
# polygon_id: p1016
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1016)
p1017 = pya.Polygon([pya.Point(0, 148), pya.Point(0, 176), pya.Point(432, 176), pya.Point(432, 148)])
# polygon_id: p1017
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1017)
p1018 = pya.Polygon([pya.Point(0, 40), pya.Point(0, 68), pya.Point(432, 68), pya.Point(432, 40)])
# polygon_id: p1018
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1018)
p1019 = pya.Polygon([pya.Point(0, 1048), pya.Point(0, 1112), pya.Point(432, 1112), pya.Point(432, 1048)])
# polygon_id: p1019
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p1019)
p1020 = pya.Polygon([pya.Point(0, -32), pya.Point(0, 32), pya.Point(432, 32), pya.Point(432, -32)])
# polygon_id: p1020
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p1020)
p1021 = pya.Polygon([pya.Point(180, 1044), pya.Point(180, 1116), pya.Point(252, 1116), pya.Point(252, 1044)])
# polygon_id: p1021
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p1021)
p1022 = pya.Polygon([pya.Point(180, -36), pya.Point(180, 36), pya.Point(252, 36), pya.Point(252, -36)])
# polygon_id: p1022
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(18, 0))).insert(p1022)
p1023 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 540), pya.Point(432, 540), pya.Point(432, 0)])
# polygon_id: p1023
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(12, 0))).insert(p1023)
p1024 = pya.Polygon([pya.Point(0, 992), pya.Point(0, 1168), pya.Point(432, 1168), pya.Point(432, 992)])
# polygon_id: p1024
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p1024)
p1025 = pya.Polygon([pya.Point(0, 452), pya.Point(0, 628), pya.Point(432, 628), pya.Point(432, 452)])
# polygon_id: p1025
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p1025)
p1026 = pya.Polygon([pya.Point(0, -88), pya.Point(0, 88), pya.Point(432, 88), pya.Point(432, -88)])
# polygon_id: p1026
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p1026)
p1027 = pya.Polygon([pya.Point(284, -20), pya.Point(284, 1100), pya.Point(364, 1100), pya.Point(364, -20)])
# polygon_id: p1027
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p1027)
p1028 = pya.Polygon([pya.Point(68, -20), pya.Point(68, 1100), pya.Point(148, 1100), pya.Point(148, -20)])
# polygon_id: p1028
cell_FILLER_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p1028)
p1033 = pya.Polygon([pya.Point(0, -36), pya.Point(0, 36), pya.Point(216, 36), pya.Point(216, -36)])
# polygon_id: p1033
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p1033)
p1034 = pya.Polygon([pya.Point(0, 1044), pya.Point(0, 1116), pya.Point(216, 1116), pya.Point(216, 1044)])
# polygon_id: p1034
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p1034)
p1035 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(216, 1080), pya.Point(216, 540)])
# polygon_id: p1035
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(13, 0))).insert(p1035)
p1036 = pya.Polygon([pya.Point(0, 540), pya.Point(0, 1080), pya.Point(216, 1080), pya.Point(216, 540)])
# polygon_id: p1036
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(1, 0))).insert(p1036)
p1037 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 1080), pya.Point(216, 1080), pya.Point(216, 0)])
# polygon_id: p1037
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(100, 0))).insert(p1037)
p1038 = pya.Polygon([pya.Point(0, 1012), pya.Point(0, 1040), pya.Point(216, 1040), pya.Point(216, 1012)])
# polygon_id: p1038
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1038)
p1039 = pya.Polygon([pya.Point(0, 904), pya.Point(0, 932), pya.Point(216, 932), pya.Point(216, 904)])
# polygon_id: p1039
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1039)
p1040 = pya.Polygon([pya.Point(0, 796), pya.Point(0, 824), pya.Point(216, 824), pya.Point(216, 796)])
# polygon_id: p1040
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1040)
p1041 = pya.Polygon([pya.Point(0, 688), pya.Point(0, 716), pya.Point(216, 716), pya.Point(216, 688)])
# polygon_id: p1041
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1041)
p1042 = pya.Polygon([pya.Point(0, 580), pya.Point(0, 608), pya.Point(216, 608), pya.Point(216, 580)])
# polygon_id: p1042
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1042)
p1043 = pya.Polygon([pya.Point(0, 472), pya.Point(0, 500), pya.Point(216, 500), pya.Point(216, 472)])
# polygon_id: p1043
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1043)
p1044 = pya.Polygon([pya.Point(0, 364), pya.Point(0, 392), pya.Point(216, 392), pya.Point(216, 364)])
# polygon_id: p1044
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1044)
p1045 = pya.Polygon([pya.Point(0, 256), pya.Point(0, 284), pya.Point(216, 284), pya.Point(216, 256)])
# polygon_id: p1045
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1045)
p1046 = pya.Polygon([pya.Point(0, 148), pya.Point(0, 176), pya.Point(216, 176), pya.Point(216, 148)])
# polygon_id: p1046
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1046)
p1047 = pya.Polygon([pya.Point(0, 40), pya.Point(0, 68), pya.Point(216, 68), pya.Point(216, 40)])
# polygon_id: p1047
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(2, 0))).insert(p1047)
p1048 = pya.Polygon([pya.Point(0, 1048), pya.Point(0, 1112), pya.Point(216, 1112), pya.Point(216, 1048)])
# polygon_id: p1048
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p1048)
p1049 = pya.Polygon([pya.Point(0, -32), pya.Point(0, 32), pya.Point(216, 32), pya.Point(216, -32)])
# polygon_id: p1049
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(16, 0))).insert(p1049)
p1050 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 540), pya.Point(216, 540), pya.Point(216, 0)])
# polygon_id: p1050
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(12, 0))).insert(p1050)
p1051 = pya.Polygon([pya.Point(0, 992), pya.Point(0, 1168), pya.Point(216, 1168), pya.Point(216, 992)])
# polygon_id: p1051
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p1051)
p1052 = pya.Polygon([pya.Point(0, 452), pya.Point(0, 628), pya.Point(216, 628), pya.Point(216, 452)])
# polygon_id: p1052
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p1052)
p1053 = pya.Polygon([pya.Point(0, -88), pya.Point(0, 88), pya.Point(216, 88), pya.Point(216, -88)])
# polygon_id: p1053
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(10, 0))).insert(p1053)
p1054 = pya.Polygon([pya.Point(68, -20), pya.Point(68, 1100), pya.Point(148, 1100), pya.Point(148, -20)])
# polygon_id: p1054
cell_FILLERxp5_ASAP7_75t_R.shapes(layout.layer(pya.LayerInfo(7, 0))).insert(p1054)
p1059 = pya.Polygon([pya.Point(2656, 3148), pya.Point(2656, 9812), pya.Point(3136, 9812), pya.Point(3136, 3148)])
# polygon_id: p1059
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p1059)
p1060 = pya.Polygon([pya.Point(1888, 2068), pya.Point(1888, 10892), pya.Point(2368, 10892), pya.Point(2368, 2068)])
# polygon_id: p1060
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p1060)
p1061 = pya.Polygon([pya.Point(3648, 2496), pya.Point(3648, 6624), pya.Point(3744, 6624), pya.Point(3744, 2496)])
# polygon_id: p1061
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p1061)
p1062 = pya.Polygon([pya.Point(4992, 10560), pya.Point(4992, 12608), pya.Point(5088, 12608), pya.Point(5088, 10560)])
# polygon_id: p1062
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p1062)
p1063 = pya.Polygon([pya.Point(5376, 11328), pya.Point(5376, 12608), pya.Point(5472, 12608), pya.Point(5472, 11328)])
# polygon_id: p1063
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p1063)
p1064 = pya.Polygon([pya.Point(5376, 64), pya.Point(5376, 1248), pya.Point(5472, 1248), pya.Point(5472, 64)])
# polygon_id: p1064
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p1064)
p1065 = pya.Polygon([pya.Point(7296, 64), pya.Point(7296, 2208), pya.Point(7392, 2208), pya.Point(7392, 64)])
# polygon_id: p1065
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p1065)
p1066 = pya.Polygon([pya.Point(4608, 11328), pya.Point(4608, 12608), pya.Point(4704, 12608), pya.Point(4704, 11328)])
# polygon_id: p1066
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p1066)
p1067 = pya.Polygon([pya.Point(5760, 10944), pya.Point(5760, 12608), pya.Point(5856, 12608), pya.Point(5856, 10944)])
# polygon_id: p1067
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p1067)
p1068 = pya.Polygon([pya.Point(5760, 64), pya.Point(5760, 1056), pya.Point(5856, 1056), pya.Point(5856, 64)])
# polygon_id: p1068
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p1068)
p1069 = pya.Polygon([pya.Point(7680, 64), pya.Point(7680, 1248), pya.Point(7776, 1248), pya.Point(7776, 64)])
# polygon_id: p1069
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p1069)
p1070 = pya.Polygon([pya.Point(4224, 11136), pya.Point(4224, 12608), pya.Point(4320, 12608), pya.Point(4320, 11136)])
# polygon_id: p1070
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p1070)
p1071 = pya.Polygon([pya.Point(6144, 9600), pya.Point(6144, 12608), pya.Point(6240, 12608), pya.Point(6240, 9600)])
# polygon_id: p1071
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p1071)
p1072 = pya.Polygon([pya.Point(7296, 10752), pya.Point(7296, 12608), pya.Point(7392, 12608), pya.Point(7392, 10752)])
# polygon_id: p1072
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p1072)
p1073 = pya.Polygon([pya.Point(6528, 64), pya.Point(6528, 1056), pya.Point(6624, 1056), pya.Point(6624, 64)])
# polygon_id: p1073
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 0))).insert(p1073)
p1074 = pya.Polygon([pya.Point(3588, 2496), pya.Point(3588, 2592), pya.Point(3744, 2592), pya.Point(3744, 2496)])
# polygon_id: p1074
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1074)
p1075 = pya.Polygon([pya.Point(3648, 6528), pya.Point(3648, 6624), pya.Point(10308, 6624), pya.Point(10308, 6528)])
# polygon_id: p1075
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1075)
p1076 = pya.Polygon([pya.Point(4884, 5184), pya.Point(4884, 5280), pya.Point(6276, 5280), pya.Point(6276, 5184)])
# polygon_id: p1076
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1076)
p1077 = pya.Polygon([pya.Point(240, 9216), pya.Point(240, 9312), pya.Point(1236, 9312), pya.Point(1236, 9216)])
# polygon_id: p1077
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1077)
p1078 = pya.Polygon([pya.Point(3300, 10560), pya.Point(3300, 10656), pya.Point(5088, 10656), pya.Point(5088, 10560)])
# polygon_id: p1078
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1078)
p1079 = pya.Polygon([pya.Point(5316, 11328), pya.Point(5316, 11424), pya.Point(5472, 11424), pya.Point(5472, 11328)])
# polygon_id: p1079
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1079)
p1080 = pya.Polygon([pya.Point(5172, 1152), pya.Point(5172, 1248), pya.Point(5472, 1248), pya.Point(5472, 1152)])
# polygon_id: p1080
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1080)
p1081 = pya.Polygon([pya.Point(6468, 2112), pya.Point(6468, 2208), pya.Point(7392, 2208), pya.Point(7392, 2112)])
# polygon_id: p1081
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1081)
p1082 = pya.Polygon([pya.Point(7188, 4992), pya.Point(7188, 5088), pya.Point(12528, 5088), pya.Point(12528, 4992)])
# polygon_id: p1082
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1082)
p1083 = pya.Polygon([pya.Point(240, 8832), pya.Point(240, 8928), pya.Point(1668, 8928), pya.Point(1668, 8832)])
# polygon_id: p1083
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1083)
p1084 = pya.Polygon([pya.Point(3012, 11328), pya.Point(3012, 11424), pya.Point(4704, 11424), pya.Point(4704, 11328)])
# polygon_id: p1084
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1084)
p1085 = pya.Polygon([pya.Point(5760, 10944), pya.Point(5760, 11040), pya.Point(6420, 11040), pya.Point(6420, 10944)])
# polygon_id: p1085
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1085)
p1086 = pya.Polygon([pya.Point(4596, 960), pya.Point(4596, 1056), pya.Point(5856, 1056), pya.Point(5856, 960)])
# polygon_id: p1086
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1086)
p1087 = pya.Polygon([pya.Point(6756, 1152), pya.Point(6756, 1248), pya.Point(7776, 1248), pya.Point(7776, 1152)])
# polygon_id: p1087
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1087)
p1088 = pya.Polygon([pya.Point(9636, 3456), pya.Point(9636, 3552), pya.Point(12528, 3552), pya.Point(12528, 3456)])
# polygon_id: p1088
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1088)
p1089 = pya.Polygon([pya.Point(240, 8448), pya.Point(240, 8544), pya.Point(1380, 8544), pya.Point(1380, 8448)])
# polygon_id: p1089
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1089)
p1090 = pya.Polygon([pya.Point(9060, 4224), pya.Point(9060, 4320), pya.Point(12528, 4320), pya.Point(12528, 4224)])
# polygon_id: p1090
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1090)
p1091 = pya.Polygon([pya.Point(3876, 5376), pya.Point(3876, 5472), pya.Point(7716, 5472), pya.Point(7716, 5376)])
# polygon_id: p1091
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1091)
p1092 = pya.Polygon([pya.Point(4164, 11136), pya.Point(4164, 11232), pya.Point(4320, 11232), pya.Point(4320, 11136)])
# polygon_id: p1092
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1092)
p1093 = pya.Polygon([pya.Point(5172, 9600), pya.Point(5172, 9696), pya.Point(6240, 9696), pya.Point(6240, 9600)])
# polygon_id: p1093
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1093)
p1094 = pya.Polygon([pya.Point(7296, 10752), pya.Point(7296, 10848), pya.Point(9156, 10848), pya.Point(9156, 10752)])
# polygon_id: p1094
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1094)
p1095 = pya.Polygon([pya.Point(6528, 960), pya.Point(6528, 1056), pya.Point(8436, 1056), pya.Point(8436, 960)])
# polygon_id: p1095
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1095)
p1096 = pya.Polygon([pya.Point(10356, 4608), pya.Point(10356, 4704), pya.Point(12528, 4704), pya.Point(12528, 4608)])
# polygon_id: p1096
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1096)
p1097 = pya.Polygon([pya.Point(10356, 3840), pya.Point(10356, 3936), pya.Point(12528, 3936), pya.Point(12528, 3840)])
# polygon_id: p1097
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1097)
p1098 = pya.Polygon([pya.Point(3440, 2496), pya.Point(3440, 2592), pya.Point(3636, 2592), pya.Point(3636, 2496)])
# polygon_id: p1098
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1098)
p1099 = pya.Polygon([pya.Point(5424, 11328), pya.Point(5424, 11424), pya.Point(5620, 11424), pya.Point(5620, 11328)])
# polygon_id: p1099
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1099)
p1100 = pya.Polygon([pya.Point(4272, 11136), pya.Point(4272, 11232), pya.Point(4468, 11232), pya.Point(4468, 11136)])
# polygon_id: p1100
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 0))).insert(p1100)
p1101 = pya.Polygon([pya.Point(2716, 9652), pya.Point(2716, 9788), pya.Point(3076, 9788), pya.Point(3076, 9652)])
# polygon_id: p1101
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1101)
p1102 = pya.Polygon([pya.Point(2716, 7492), pya.Point(2716, 7628), pya.Point(3076, 7628), pya.Point(3076, 7492)])
# polygon_id: p1102
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1102)
p1103 = pya.Polygon([pya.Point(2716, 5332), pya.Point(2716, 5468), pya.Point(3076, 5468), pya.Point(3076, 5332)])
# polygon_id: p1103
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1103)
p1104 = pya.Polygon([pya.Point(2716, 3172), pya.Point(2716, 3308), pya.Point(3076, 3308), pya.Point(3076, 3172)])
# polygon_id: p1104
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1104)
p1105 = pya.Polygon([pya.Point(1948, 10732), pya.Point(1948, 10868), pya.Point(2308, 10868), pya.Point(2308, 10732)])
# polygon_id: p1105
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1105)
p1106 = pya.Polygon([pya.Point(1948, 8572), pya.Point(1948, 8708), pya.Point(2308, 8708), pya.Point(2308, 8572)])
# polygon_id: p1106
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1106)
p1107 = pya.Polygon([pya.Point(1948, 6412), pya.Point(1948, 6548), pya.Point(2308, 6548), pya.Point(2308, 6412)])
# polygon_id: p1107
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1107)
p1108 = pya.Polygon([pya.Point(1948, 4252), pya.Point(1948, 4388), pya.Point(2308, 4388), pya.Point(2308, 4252)])
# polygon_id: p1108
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1108)
p1109 = pya.Polygon([pya.Point(1948, 2092), pya.Point(1948, 2228), pya.Point(2308, 2228), pya.Point(2308, 2092)])
# polygon_id: p1109
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1109)
p1110 = pya.Polygon([pya.Point(4752, 4896), pya.Point(4752, 9936), pya.Point(4824, 9936), pya.Point(4824, 4896)])
# polygon_id: p1110
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1110)
p1111 = pya.Polygon([pya.Point(3600, 2448), pya.Point(3600, 2580), pya.Point(3672, 2580), pya.Point(3672, 2448)])
# polygon_id: p1111
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1111)
p1112 = pya.Polygon([pya.Point(10224, 6540), pya.Point(10224, 6696), pya.Point(10296, 6696), pya.Point(10296, 6540)])
# polygon_id: p1112
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1112)
p1113 = pya.Polygon([pya.Point(8064, 5040), pya.Point(8064, 5616), pya.Point(8136, 5616), pya.Point(8136, 5040)])
# polygon_id: p1113
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1113)
p1114 = pya.Polygon([pya.Point(9360, 6120), pya.Point(9360, 6696), pya.Point(9432, 6696), pya.Point(9432, 6120)])
# polygon_id: p1114
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1114)
p1115 = pya.Polygon([pya.Point(9216, 7344), pya.Point(9216, 7920), pya.Point(9288, 7920), pya.Point(9288, 7344)])
# polygon_id: p1115
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1115)
p1116 = pya.Polygon([pya.Point(8928, 3816), pya.Point(8928, 8856), pya.Point(9000, 8856), pya.Point(9000, 3816)])
# polygon_id: p1116
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1116)
p1117 = pya.Polygon([pya.Point(2448, 6120), pya.Point(2448, 7416), pya.Point(2520, 7416), pya.Point(2520, 6120)])
# polygon_id: p1117
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1117)
p1118 = pya.Polygon([pya.Point(4320, 5544), pya.Point(4320, 10656), pya.Point(4392, 10656), pya.Point(4392, 5544)])
# polygon_id: p1118
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1118)
p1119 = pya.Polygon([pya.Point(4032, 3960), pya.Point(4032, 4536), pya.Point(4104, 4536), pya.Point(4104, 3960)])
# polygon_id: p1119
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1119)
p1120 = pya.Polygon([pya.Point(4608, 4104), pya.Point(4608, 6984), pya.Point(4680, 6984), pya.Point(4680, 4104)])
# polygon_id: p1120
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1120)
p1121 = pya.Polygon([pya.Point(6768, 3384), pya.Point(6768, 6192), pya.Point(6840, 6192), pya.Point(6840, 3384)])
# polygon_id: p1121
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1121)
p1122 = pya.Polygon([pya.Point(5472, 4608), pya.Point(5472, 6696), pya.Point(5544, 6696), pya.Point(5544, 4608)])
# polygon_id: p1122
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1122)
p1123 = pya.Polygon([pya.Point(8640, 4464), pya.Point(8640, 6696), pya.Point(8712, 6696), pya.Point(8712, 4464)])
# polygon_id: p1123
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1123)
p1124 = pya.Polygon([pya.Point(6624, 7344), pya.Point(6624, 8352), pya.Point(6696, 8352), pya.Point(6696, 7344)])
# polygon_id: p1124
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1124)
p1125 = pya.Polygon([pya.Point(7920, 7344), pya.Point(7920, 7776), pya.Point(7992, 7776), pya.Point(7992, 7344)])
# polygon_id: p1125
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1125)
p1126 = pya.Polygon([pya.Point(7488, 8928), pya.Point(7488, 10368), pya.Point(7560, 10368), pya.Point(7560, 8928)])
# polygon_id: p1126
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1126)
p1127 = pya.Polygon([pya.Point(3744, 3816), pya.Point(3744, 7416), pya.Point(3816, 7416), pya.Point(3816, 3816)])
# polygon_id: p1127
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1127)
p1128 = pya.Polygon([pya.Point(4896, 5184), pya.Point(4896, 5268), pya.Point(4968, 5268), pya.Point(4968, 5184)])
# polygon_id: p1128
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1128)
p1129 = pya.Polygon([pya.Point(6192, 5196), pya.Point(6192, 6048), pya.Point(6264, 6048), pya.Point(6264, 5196)])
# polygon_id: p1129
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1129)
p1130 = pya.Polygon([pya.Point(6624, 4104), pya.Point(6624, 4824), pya.Point(6696, 4824), pya.Point(6696, 4104)])
# polygon_id: p1130
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1130)
p1131 = pya.Polygon([pya.Point(7056, 6624), pya.Point(7056, 8208), pya.Point(7128, 8208), pya.Point(7128, 6624)])
# polygon_id: p1131
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1131)
p1132 = pya.Polygon([pya.Point(7200, 7344), pya.Point(7200, 9288), pya.Point(7272, 9288), pya.Point(7272, 7344)])
# polygon_id: p1132
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1132)
p1133 = pya.Polygon([pya.Point(1152, 9216), pya.Point(1152, 9300), pya.Point(1224, 9300), pya.Point(1224, 9216)])
# polygon_id: p1133
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1133)
p1134 = pya.Polygon([pya.Point(3312, 10440), pya.Point(3312, 10644), pya.Point(3384, 10644), pya.Point(3384, 10440)])
# polygon_id: p1134
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1134)
p1135 = pya.Polygon([pya.Point(5328, 10440), pya.Point(5328, 11412), pya.Point(5400, 11412), pya.Point(5400, 10440)])
# polygon_id: p1135
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1135)
p1136 = pya.Polygon([pya.Point(5184, 1164), pya.Point(5184, 2808), pya.Point(5256, 2808), pya.Point(5256, 1164)])
# polygon_id: p1136
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1136)
p1137 = pya.Polygon([pya.Point(6480, 2124), pya.Point(6480, 2664), pya.Point(6552, 2664), pya.Point(6552, 2124)])
# polygon_id: p1137
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1137)
p1138 = pya.Polygon([pya.Point(7200, 3960), pya.Point(7200, 5076), pya.Point(7272, 5076), pya.Point(7272, 3960)])
# polygon_id: p1138
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1138)
p1139 = pya.Polygon([pya.Point(1584, 7056), pya.Point(1584, 8916), pya.Point(1656, 8916), pya.Point(1656, 7056)])
# polygon_id: p1139
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1139)
p1140 = pya.Polygon([pya.Point(3024, 10440), pya.Point(3024, 11412), pya.Point(3096, 11412), pya.Point(3096, 10440)])
# polygon_id: p1140
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1140)
p1141 = pya.Polygon([pya.Point(6336, 10440), pya.Point(6336, 11028), pya.Point(6408, 11028), pya.Point(6408, 10440)])
# polygon_id: p1141
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1141)
p1142 = pya.Polygon([pya.Point(4608, 972), pya.Point(4608, 2520), pya.Point(4680, 2520), pya.Point(4680, 972)])
# polygon_id: p1142
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1142)
p1143 = pya.Polygon([pya.Point(6768, 1164), pya.Point(6768, 2520), pya.Point(6840, 2520), pya.Point(6840, 1164)])
# polygon_id: p1143
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1143)
p1144 = pya.Polygon([pya.Point(9648, 2880), pya.Point(9648, 3540), pya.Point(9720, 3540), pya.Point(9720, 2880)])
# polygon_id: p1144
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1144)
p1145 = pya.Polygon([pya.Point(1296, 8424), pya.Point(1296, 8532), pya.Point(1368, 8532), pya.Point(1368, 8424)])
# polygon_id: p1145
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1145)
p1146 = pya.Polygon([pya.Point(9072, 4104), pya.Point(9072, 4308), pya.Point(9144, 4308), pya.Point(9144, 4104)])
# polygon_id: p1146
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1146)
p1147 = pya.Polygon([pya.Point(3312, 5688), pya.Point(3312, 8856), pya.Point(3384, 8856), pya.Point(3384, 5688)])
# polygon_id: p1147
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1147)
p1148 = pya.Polygon([pya.Point(6480, 3024), pya.Point(6480, 4968), pya.Point(6552, 4968), pya.Point(6552, 3024)])
# polygon_id: p1148
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1148)
p1149 = pya.Polygon([pya.Point(7344, 3024), pya.Point(7344, 8064), pya.Point(7416, 8064), pya.Point(7416, 3024)])
# polygon_id: p1149
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1149)
p1150 = pya.Polygon([pya.Point(10080, 3024), pya.Point(10080, 9432), pya.Point(10152, 9432), pya.Point(10152, 3024)])
# polygon_id: p1150
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1150)
p1151 = pya.Polygon([pya.Point(5184, 5832), pya.Point(5184, 7776), pya.Point(5256, 7776), pya.Point(5256, 5832)])
# polygon_id: p1151
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1151)
p1152 = pya.Polygon([pya.Point(9936, 3528), pya.Point(9936, 9936), pya.Point(10008, 9936), pya.Point(10008, 3528)])
# polygon_id: p1152
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1152)
p1153 = pya.Polygon([pya.Point(3888, 5184), pya.Point(3888, 5460), pya.Point(3960, 5460), pya.Point(3960, 5184)])
# polygon_id: p1153
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1153)
p1154 = pya.Polygon([pya.Point(7632, 5388), pya.Point(7632, 10080), pya.Point(7704, 10080), pya.Point(7704, 5388)])
# polygon_id: p1154
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1154)
p1155 = pya.Polygon([pya.Point(4464, 3024), pya.Point(4464, 9000), pya.Point(4536, 9000), pya.Point(4536, 3024)])
# polygon_id: p1155
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1155)
p1156 = pya.Polygon([pya.Point(8496, 5184), pya.Point(8496, 10080), pya.Point(8568, 10080), pya.Point(8568, 5184)])
# polygon_id: p1156
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1156)
p1157 = pya.Polygon([pya.Point(8352, 2880), pya.Point(8352, 4968), pya.Point(8424, 4968), pya.Point(8424, 2880)])
# polygon_id: p1157
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1157)
p1158 = pya.Polygon([pya.Point(9072, 4896), pya.Point(9072, 5616), pya.Point(9144, 5616), pya.Point(9144, 4896)])
# polygon_id: p1158
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1158)
p1159 = pya.Polygon([pya.Point(9648, 5040), pya.Point(9648, 7776), pya.Point(9720, 7776), pya.Point(9720, 5040)])
# polygon_id: p1159
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1159)
p1160 = pya.Polygon([pya.Point(4176, 3528), pya.Point(4176, 9936), pya.Point(4248, 9936), pya.Point(4248, 3528)])
# polygon_id: p1160
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1160)
p1161 = pya.Polygon([pya.Point(6480, 5688), pya.Point(6480, 9936), pya.Point(6552, 9936), pya.Point(6552, 5688)])
# polygon_id: p1161
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1161)
p1162 = pya.Polygon([pya.Point(4320, 2880), pya.Point(4320, 4536), pya.Point(4392, 4536), pya.Point(4392, 2880)])
# polygon_id: p1162
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1162)
p1163 = pya.Polygon([pya.Point(5184, 4464), pya.Point(5184, 5112), pya.Point(5256, 5112), pya.Point(5256, 4464)])
# polygon_id: p1163
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1163)
p1164 = pya.Polygon([pya.Point(6336, 2304), pya.Point(6336, 7920), pya.Point(6408, 7920), pya.Point(6408, 2304)])
# polygon_id: p1164
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1164)
p1165 = pya.Polygon([pya.Point(7344, 8784), pya.Point(7344, 9144), pya.Point(7416, 9144), pya.Point(7416, 8784)])
# polygon_id: p1165
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1165)
p1166 = pya.Polygon([pya.Point(7776, 4104), pya.Point(7776, 8856), pya.Point(7848, 8856), pya.Point(7848, 4104)])
# polygon_id: p1166
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1166)
p1167 = pya.Polygon([pya.Point(3888, 5976), pya.Point(3888, 6696), pya.Point(3960, 6696), pya.Point(3960, 5976)])
# polygon_id: p1167
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1167)
p1168 = pya.Polygon([pya.Point(3456, 3672), pya.Point(3456, 9936), pya.Point(3528, 9936), pya.Point(3528, 3672)])
# polygon_id: p1168
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1168)
p1169 = pya.Polygon([pya.Point(6912, 5832), pya.Point(6912, 9936), pya.Point(6984, 9936), pya.Point(6984, 5832)])
# polygon_id: p1169
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1169)
p1170 = pya.Polygon([pya.Point(4176, 10944), pya.Point(4176, 11220), pya.Point(4248, 11220), pya.Point(4248, 10944)])
# polygon_id: p1170
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1170)
p1171 = pya.Polygon([pya.Point(7920, 10584), pya.Point(7920, 11016), pya.Point(7992, 11016), pya.Point(7992, 10584)])
# polygon_id: p1171
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1171)
p1172 = pya.Polygon([pya.Point(5184, 9504), pya.Point(5184, 9684), pya.Point(5256, 9684), pya.Point(5256, 9504)])
# polygon_id: p1172
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1172)
p1173 = pya.Polygon([pya.Point(9072, 10584), pya.Point(9072, 10836), pya.Point(9144, 10836), pya.Point(9144, 10584)])
# polygon_id: p1173
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1173)
p1174 = pya.Polygon([pya.Point(8352, 972), pya.Point(8352, 2376), pya.Point(8424, 2376), pya.Point(8424, 972)])
# polygon_id: p1174
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1174)
p1175 = pya.Polygon([pya.Point(10368, 4464), pya.Point(10368, 4692), pya.Point(10440, 4692), pya.Point(10440, 4464)])
# polygon_id: p1175
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1175)
p1176 = pya.Polygon([pya.Point(10368, 3852), pya.Point(10368, 4176), pya.Point(10440, 4176), pya.Point(10440, 3852)])
# polygon_id: p1176
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1176)
p1177 = pya.Polygon([pya.Point(4896, 5140), pya.Point(4896, 5220), pya.Point(4968, 5220), pya.Point(4968, 5140)])
# polygon_id: p1177
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1177)
p1178 = pya.Polygon([pya.Point(1152, 9264), pya.Point(1152, 9344), pya.Point(1224, 9344), pya.Point(1224, 9264)])
# polygon_id: p1178
cell_Block3.shapes(layout.layer(pya.LayerInfo(30, 0))).insert(p1178)
p1179 = pya.Polygon([pya.Point(1728, 9684), pya.Point(1728, 9756), pya.Point(11016, 9756), pya.Point(11016, 9684)])
# polygon_id: p1179
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1179)
p1180 = pya.Polygon([pya.Point(1728, 7524), pya.Point(1728, 7596), pya.Point(11016, 7596), pya.Point(11016, 7524)])
# polygon_id: p1180
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1180)
p1181 = pya.Polygon([pya.Point(1728, 5364), pya.Point(1728, 5436), pya.Point(11016, 5436), pya.Point(11016, 5364)])
# polygon_id: p1181
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1181)
p1182 = pya.Polygon([pya.Point(1728, 3204), pya.Point(1728, 3276), pya.Point(11016, 3276), pya.Point(11016, 3204)])
# polygon_id: p1182
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1182)
p1183 = pya.Polygon([pya.Point(1728, 10764), pya.Point(1728, 10836), pya.Point(11016, 10836), pya.Point(11016, 10764)])
# polygon_id: p1183
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1183)
p1184 = pya.Polygon([pya.Point(1728, 8604), pya.Point(1728, 8676), pya.Point(11016, 8676), pya.Point(11016, 8604)])
# polygon_id: p1184
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1184)
p1185 = pya.Polygon([pya.Point(1728, 6444), pya.Point(1728, 6516), pya.Point(11016, 6516), pya.Point(11016, 6444)])
# polygon_id: p1185
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1185)
p1186 = pya.Polygon([pya.Point(1728, 4284), pya.Point(1728, 4356), pya.Point(11016, 4356), pya.Point(11016, 4284)])
# polygon_id: p1186
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1186)
p1187 = pya.Polygon([pya.Point(1728, 2124), pya.Point(1728, 2196), pya.Point(11016, 2196), pya.Point(11016, 2124)])
# polygon_id: p1187
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1187)
p1188 = pya.Polygon([pya.Point(2880, 4896), pya.Point(2880, 4968), pya.Point(4824, 4968), pya.Point(4824, 4896)])
# polygon_id: p1188
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1188)
p1189 = pya.Polygon([pya.Point(8064, 5544), pya.Point(8064, 5616), pya.Point(8712, 5616), pya.Point(8712, 5544)])
# polygon_id: p1189
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1189)
p1190 = pya.Polygon([pya.Point(9216, 6120), pya.Point(9216, 6192), pya.Point(9432, 6192), pya.Point(9432, 6120)])
# polygon_id: p1190
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1190)
p1191 = pya.Polygon([pya.Point(8208, 7344), pya.Point(8208, 7416), pya.Point(9288, 7416), pya.Point(9288, 7344)])
# polygon_id: p1191
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1191)
p1192 = pya.Polygon([pya.Point(8928, 3816), pya.Point(8928, 3888), pya.Point(9432, 3888), pya.Point(9432, 3816)])
# polygon_id: p1192
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1192)
p1193 = pya.Polygon([pya.Point(2304, 7344), pya.Point(2304, 7416), pya.Point(2520, 7416), pya.Point(2520, 7344)])
# polygon_id: p1193
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1193)
p1194 = pya.Polygon([pya.Point(2448, 6120), pya.Point(2448, 6192), pya.Point(2772, 6192), pya.Point(2772, 6120)])
# polygon_id: p1194
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1194)
p1195 = pya.Polygon([pya.Point(4032, 5544), pya.Point(4032, 5616), pya.Point(4392, 5616), pya.Point(4392, 5544)])
# polygon_id: p1195
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1195)
p1196 = pya.Polygon([pya.Point(4320, 10584), pya.Point(4320, 10656), pya.Point(4536, 10656), pya.Point(4536, 10584)])
# polygon_id: p1196
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1196)
p1197 = pya.Polygon([pya.Point(4464, 4104), pya.Point(4464, 4176), pya.Point(4680, 4176), pya.Point(4680, 4104)])
# polygon_id: p1197
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1197)
p1198 = pya.Polygon([pya.Point(4608, 6912), pya.Point(4608, 6984), pya.Point(9864, 6984), pya.Point(9864, 6912)])
# polygon_id: p1198
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1198)
p1199 = pya.Polygon([pya.Point(6192, 3384), pya.Point(6192, 3456), pya.Point(6840, 3456), pya.Point(6840, 3384)])
# polygon_id: p1199
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1199)
p1200 = pya.Polygon([pya.Point(7056, 6264), pya.Point(7056, 6336), pya.Point(8424, 6336), pya.Point(8424, 6264)])
# polygon_id: p1200
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1200)
p1201 = pya.Polygon([pya.Point(5328, 6624), pya.Point(5328, 6696), pya.Point(5544, 6696), pya.Point(5544, 6624)])
# polygon_id: p1201
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1201)
p1202 = pya.Polygon([pya.Point(6624, 4464), pya.Point(6624, 4536), pya.Point(8712, 4536), pya.Point(8712, 4464)])
# polygon_id: p1202
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1202)
p1203 = pya.Polygon([pya.Point(8640, 6624), pya.Point(8640, 6696), pya.Point(9000, 6696), pya.Point(9000, 6624)])
# polygon_id: p1203
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1203)
p1204 = pya.Polygon([pya.Point(6624, 7344), pya.Point(6624, 7416), pya.Point(6840, 7416), pya.Point(6840, 7344)])
# polygon_id: p1204
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1204)
p1205 = pya.Polygon([pya.Point(7488, 10296), pya.Point(7488, 10368), pya.Point(9648, 10368), pya.Point(9648, 10296)])
# polygon_id: p1205
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1205)
p1206 = pya.Polygon([pya.Point(7344, 9504), pya.Point(7344, 9576), pya.Point(8568, 9576), pya.Point(8568, 9504)])
# polygon_id: p1206
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1206)
p1207 = pya.Polygon([pya.Point(3024, 7344), pya.Point(3024, 7416), pya.Point(3816, 7416), pya.Point(3816, 7344)])
# polygon_id: p1207
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1207)
p1208 = pya.Polygon([pya.Point(4752, 5184), pya.Point(4752, 5256), pya.Point(4968, 5256), pya.Point(4968, 5184)])
# polygon_id: p1208
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1208)
p1209 = pya.Polygon([pya.Point(6048, 6624), pya.Point(6048, 6696), pya.Point(7128, 6696), pya.Point(7128, 6624)])
# polygon_id: p1209
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1209)
p1210 = pya.Polygon([pya.Point(1152, 9216), pya.Point(1152, 9288), pya.Point(2304, 9288), pya.Point(2304, 9216)])
# polygon_id: p1210
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1210)
p1211 = pya.Polygon([pya.Point(2448, 2736), pya.Point(2448, 2808), pya.Point(5256, 2808), pya.Point(5256, 2736)])
# polygon_id: p1211
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1211)
p1212 = pya.Polygon([pya.Point(5688, 2592), pya.Point(5688, 2664), pya.Point(6552, 2664), pya.Point(6552, 2592)])
# polygon_id: p1212
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1212)
p1213 = pya.Polygon([pya.Point(1584, 7056), pya.Point(1584, 7128), pya.Point(3384, 7128), pya.Point(3384, 7056)])
# polygon_id: p1213
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1213)
p1214 = pya.Polygon([pya.Point(2304, 10440), pya.Point(2304, 10512), pya.Point(3096, 10512), pya.Point(3096, 10440)])
# polygon_id: p1214
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1214)
p1215 = pya.Polygon([pya.Point(1296, 8424), pya.Point(1296, 8496), pya.Point(2304, 8496), pya.Point(2304, 8424)])
# polygon_id: p1215
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1215)
p1216 = pya.Polygon([pya.Point(5472, 3024), pya.Point(5472, 3096), pya.Point(6552, 3096), pya.Point(6552, 3024)])
# polygon_id: p1216
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1216)
p1217 = pya.Polygon([pya.Point(7812, 9360), pya.Point(7812, 9432), pya.Point(10152, 9432), pya.Point(10152, 9360)])
# polygon_id: p1217
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1217)
p1218 = pya.Polygon([pya.Point(4788, 5832), pya.Point(4788, 5904), pya.Point(5256, 5904), pya.Point(5256, 5832)])
# polygon_id: p1218
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1218)
p1219 = pya.Polygon([pya.Point(8352, 3528), pya.Point(8352, 3600), pya.Point(10008, 3600), pya.Point(10008, 3528)])
# polygon_id: p1219
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1219)
p1220 = pya.Polygon([pya.Point(3744, 5184), pya.Point(3744, 5256), pya.Point(3960, 5256), pya.Point(3960, 5184)])
# polygon_id: p1220
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1220)
p1221 = pya.Polygon([pya.Point(7488, 10008), pya.Point(7488, 10080), pya.Point(7704, 10080), pya.Point(7704, 10008)])
# polygon_id: p1221
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1221)
p1222 = pya.Polygon([pya.Point(4176, 3024), pya.Point(4176, 3096), pya.Point(4536, 3096), pya.Point(4536, 3024)])
# polygon_id: p1222
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1222)
p1223 = pya.Polygon([pya.Point(8496, 5184), pya.Point(8496, 5256), pya.Point(8712, 5256), pya.Point(8712, 5184)])
# polygon_id: p1223
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1223)
p1224 = pya.Polygon([pya.Point(7920, 2880), pya.Point(7920, 2952), pya.Point(8424, 2952), pya.Point(8424, 2880)])
# polygon_id: p1224
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1224)
p1225 = pya.Polygon([pya.Point(8352, 4896), pya.Point(8352, 4968), pya.Point(9144, 4968), pya.Point(9144, 4896)])
# polygon_id: p1225
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1225)
p1226 = pya.Polygon([pya.Point(9072, 5544), pya.Point(9072, 5616), pya.Point(9720, 5616), pya.Point(9720, 5544)])
# polygon_id: p1226
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1226)
p1227 = pya.Polygon([pya.Point(6048, 9864), pya.Point(6048, 9936), pya.Point(6552, 9936), pya.Point(6552, 9864)])
# polygon_id: p1227
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1227)
p1228 = pya.Polygon([pya.Point(3312, 2880), pya.Point(3312, 2952), pya.Point(4392, 2952), pya.Point(4392, 2880)])
# polygon_id: p1228
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1228)
p1229 = pya.Polygon([pya.Point(4320, 4464), pya.Point(4320, 4536), pya.Point(5256, 4536), pya.Point(5256, 4464)])
# polygon_id: p1229
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1229)
p1230 = pya.Polygon([pya.Point(7344, 8784), pya.Point(7344, 8856), pya.Point(7848, 8856), pya.Point(7848, 8784)])
# polygon_id: p1230
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1230)
p1231 = pya.Polygon([pya.Point(3024, 9864), pya.Point(3024, 9936), pya.Point(3528, 9936), pya.Point(3528, 9864)])
# polygon_id: p1231
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1231)
p1232 = pya.Polygon([pya.Point(4176, 10944), pya.Point(4176, 11016), pya.Point(7992, 11016), pya.Point(7992, 10944)])
# polygon_id: p1232
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1232)
p1233 = pya.Polygon([pya.Point(4696, 9864), pya.Point(4696, 9936), pya.Point(4788, 9936), pya.Point(4788, 9864)])
# polygon_id: p1233
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1233)
p1234 = pya.Polygon([pya.Point(3544, 2448), pya.Point(3544, 2520), pya.Point(3636, 2520), pya.Point(3636, 2448)])
# polygon_id: p1234
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1234)
p1235 = pya.Polygon([pya.Point(10168, 6624), pya.Point(10168, 6696), pya.Point(10260, 6696), pya.Point(10260, 6624)])
# polygon_id: p1235
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1235)
p1236 = pya.Polygon([pya.Point(8008, 5040), pya.Point(8008, 5112), pya.Point(8100, 5112), pya.Point(8100, 5040)])
# polygon_id: p1236
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1236)
p1237 = pya.Polygon([pya.Point(9304, 6624), pya.Point(9304, 6696), pya.Point(9396, 6696), pya.Point(9396, 6624)])
# polygon_id: p1237
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1237)
p1238 = pya.Polygon([pya.Point(9160, 7848), pya.Point(9160, 7920), pya.Point(9252, 7920), pya.Point(9252, 7848)])
# polygon_id: p1238
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1238)
p1239 = pya.Polygon([pya.Point(8872, 8784), pya.Point(8872, 8856), pya.Point(8964, 8856), pya.Point(8964, 8784)])
# polygon_id: p1239
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1239)
p1240 = pya.Polygon([pya.Point(3976, 4464), pya.Point(3976, 4536), pya.Point(4068, 4536), pya.Point(4068, 4464)])
# polygon_id: p1240
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1240)
p1241 = pya.Polygon([pya.Point(7864, 7344), pya.Point(7864, 7416), pya.Point(7956, 7416), pya.Point(7956, 7344)])
# polygon_id: p1241
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1241)
p1242 = pya.Polygon([pya.Point(7864, 7704), pya.Point(7864, 7776), pya.Point(7956, 7776), pya.Point(7956, 7704)])
# polygon_id: p1242
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1242)
p1243 = pya.Polygon([pya.Point(6568, 4104), pya.Point(6568, 4176), pya.Point(6660, 4176), pya.Point(6660, 4104)])
# polygon_id: p1243
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1243)
p1244 = pya.Polygon([pya.Point(7144, 7344), pya.Point(7144, 7416), pya.Point(7236, 7416), pya.Point(7236, 7344)])
# polygon_id: p1244
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1244)
p1245 = pya.Polygon([pya.Point(3256, 10440), pya.Point(3256, 10512), pya.Point(3348, 10512), pya.Point(3348, 10440)])
# polygon_id: p1245
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1245)
p1246 = pya.Polygon([pya.Point(5272, 10440), pya.Point(5272, 10512), pya.Point(5364, 10512), pya.Point(5364, 10440)])
# polygon_id: p1246
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1246)
p1247 = pya.Polygon([pya.Point(7144, 3960), pya.Point(7144, 4032), pya.Point(7236, 4032), pya.Point(7236, 3960)])
# polygon_id: p1247
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1247)
p1248 = pya.Polygon([pya.Point(6280, 10440), pya.Point(6280, 10512), pya.Point(6372, 10512), pya.Point(6372, 10440)])
# polygon_id: p1248
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1248)
p1249 = pya.Polygon([pya.Point(4552, 2448), pya.Point(4552, 2520), pya.Point(4644, 2520), pya.Point(4644, 2448)])
# polygon_id: p1249
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1249)
p1250 = pya.Polygon([pya.Point(6712, 2448), pya.Point(6712, 2520), pya.Point(6804, 2520), pya.Point(6804, 2448)])
# polygon_id: p1250
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1250)
p1251 = pya.Polygon([pya.Point(9592, 2880), pya.Point(9592, 2952), pya.Point(9684, 2952), pya.Point(9684, 2880)])
# polygon_id: p1251
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1251)
p1252 = pya.Polygon([pya.Point(9016, 4104), pya.Point(9016, 4176), pya.Point(9108, 4176), pya.Point(9108, 4104)])
# polygon_id: p1252
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1252)
p1253 = pya.Polygon([pya.Point(3256, 8784), pya.Point(3256, 8856), pya.Point(3348, 8856), pya.Point(3348, 8784)])
# polygon_id: p1253
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1253)
p1254 = pya.Polygon([pya.Point(7288, 3024), pya.Point(7288, 3096), pya.Point(7380, 3096), pya.Point(7380, 3024)])
# polygon_id: p1254
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1254)
p1255 = pya.Polygon([pya.Point(10024, 3024), pya.Point(10024, 3096), pya.Point(10116, 3096), pya.Point(10116, 3024)])
# polygon_id: p1255
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1255)
p1256 = pya.Polygon([pya.Point(5128, 7704), pya.Point(5128, 7776), pya.Point(5220, 7776), pya.Point(5220, 7704)])
# polygon_id: p1256
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1256)
p1257 = pya.Polygon([pya.Point(9880, 9864), pya.Point(9880, 9936), pya.Point(9972, 9936), pya.Point(9972, 9864)])
# polygon_id: p1257
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1257)
p1258 = pya.Polygon([pya.Point(4500, 8928), pya.Point(4500, 9000), pya.Point(4592, 9000), pya.Point(4592, 8928)])
# polygon_id: p1258
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1258)
p1259 = pya.Polygon([pya.Point(8440, 10008), pya.Point(8440, 10080), pya.Point(8532, 10080), pya.Point(8532, 10008)])
# polygon_id: p1259
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1259)
p1260 = pya.Polygon([pya.Point(9592, 5040), pya.Point(9592, 5112), pya.Point(9684, 5112), pya.Point(9684, 5040)])
# polygon_id: p1260
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1260)
p1261 = pya.Polygon([pya.Point(9592, 7704), pya.Point(9592, 7776), pya.Point(9684, 7776), pya.Point(9684, 7704)])
# polygon_id: p1261
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1261)
p1262 = pya.Polygon([pya.Point(4120, 9864), pya.Point(4120, 9936), pya.Point(4212, 9936), pya.Point(4212, 9864)])
# polygon_id: p1262
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1262)
p1263 = pya.Polygon([pya.Point(6280, 2304), pya.Point(6280, 2376), pya.Point(6372, 2376), pya.Point(6372, 2304)])
# polygon_id: p1263
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1263)
p1264 = pya.Polygon([pya.Point(7720, 4104), pya.Point(7720, 4176), pya.Point(7812, 4176), pya.Point(7812, 4104)])
# polygon_id: p1264
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1264)
p1265 = pya.Polygon([pya.Point(3832, 6624), pya.Point(3832, 6696), pya.Point(3924, 6696), pya.Point(3924, 6624)])
# polygon_id: p1265
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1265)
p1266 = pya.Polygon([pya.Point(6856, 9864), pya.Point(6856, 9936), pya.Point(6948, 9936), pya.Point(6948, 9864)])
# polygon_id: p1266
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1266)
p1267 = pya.Polygon([pya.Point(7864, 10584), pya.Point(7864, 10656), pya.Point(7956, 10656), pya.Point(7956, 10584)])
# polygon_id: p1267
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1267)
p1268 = pya.Polygon([pya.Point(5128, 9504), pya.Point(5128, 9576), pya.Point(5220, 9576), pya.Point(5220, 9504)])
# polygon_id: p1268
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1268)
p1269 = pya.Polygon([pya.Point(9016, 10584), pya.Point(9016, 10656), pya.Point(9108, 10656), pya.Point(9108, 10584)])
# polygon_id: p1269
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1269)
p1270 = pya.Polygon([pya.Point(8296, 2304), pya.Point(8296, 2376), pya.Point(8388, 2376), pya.Point(8388, 2304)])
# polygon_id: p1270
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1270)
p1271 = pya.Polygon([pya.Point(10312, 4464), pya.Point(10312, 4536), pya.Point(10404, 4536), pya.Point(10404, 4464)])
# polygon_id: p1271
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1271)
p1272 = pya.Polygon([pya.Point(10312, 4104), pya.Point(10312, 4176), pya.Point(10404, 4176), pya.Point(10404, 4104)])
# polygon_id: p1272
cell_Block3.shapes(layout.layer(pya.LayerInfo(20, 0))).insert(p1272)
p1273 = pya.Polygon([pya.Point(1728, 9684), pya.Point(1728, 9756), pya.Point(11016, 9756), pya.Point(11016, 9684)])
# polygon_id: p1273
cell_Block3.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p1273)
p1274 = pya.Polygon([pya.Point(1728, 7524), pya.Point(1728, 7596), pya.Point(11016, 7596), pya.Point(11016, 7524)])
# polygon_id: p1274
cell_Block3.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p1274)
p1275 = pya.Polygon([pya.Point(1728, 5364), pya.Point(1728, 5436), pya.Point(11016, 5436), pya.Point(11016, 5364)])
# polygon_id: p1275
cell_Block3.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p1275)
p1276 = pya.Polygon([pya.Point(1728, 3204), pya.Point(1728, 3276), pya.Point(11016, 3276), pya.Point(11016, 3204)])
# polygon_id: p1276
cell_Block3.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p1276)
p1277 = pya.Polygon([pya.Point(1728, 10764), pya.Point(1728, 10836), pya.Point(11016, 10836), pya.Point(11016, 10764)])
# polygon_id: p1277
cell_Block3.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p1277)
p1278 = pya.Polygon([pya.Point(1728, 8604), pya.Point(1728, 8676), pya.Point(11016, 8676), pya.Point(11016, 8604)])
# polygon_id: p1278
cell_Block3.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p1278)
p1279 = pya.Polygon([pya.Point(1728, 6444), pya.Point(1728, 6516), pya.Point(11016, 6516), pya.Point(11016, 6444)])
# polygon_id: p1279
cell_Block3.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p1279)
p1280 = pya.Polygon([pya.Point(1728, 4284), pya.Point(1728, 4356), pya.Point(11016, 4356), pya.Point(11016, 4284)])
# polygon_id: p1280
cell_Block3.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p1280)
p1281 = pya.Polygon([pya.Point(1728, 2124), pya.Point(1728, 2196), pya.Point(11016, 2196), pya.Point(11016, 2124)])
# polygon_id: p1281
cell_Block3.shapes(layout.layer(pya.LayerInfo(19, 0))).insert(p1281)
p1282 = pya.Polygon([pya.Point(0, 0), pya.Point(0, 12696), pya.Point(12696, 12696), pya.Point(12696, 0)])
# polygon_id: p1282
cell_Block3.shapes(layout.layer(pya.LayerInfo(235, 0))).insert(p1282)
p1283 = pya.Polygon([pya.Point(0, 9216), pya.Point(0, 9312), pya.Point(336, 9312), pya.Point(336, 9216)])
# polygon_id: p1283
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 251))).insert(p1283)
p1284 = pya.Polygon([pya.Point(12360, 4992), pya.Point(12360, 5088), pya.Point(12696, 5088), pya.Point(12696, 4992)])
# polygon_id: p1284
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 251))).insert(p1284)
p1285 = pya.Polygon([pya.Point(0, 8832), pya.Point(0, 8928), pya.Point(336, 8928), pya.Point(336, 8832)])
# polygon_id: p1285
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 251))).insert(p1285)
p1286 = pya.Polygon([pya.Point(12360, 3456), pya.Point(12360, 3552), pya.Point(12696, 3552), pya.Point(12696, 3456)])
# polygon_id: p1286
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 251))).insert(p1286)
p1287 = pya.Polygon([pya.Point(0, 8448), pya.Point(0, 8544), pya.Point(336, 8544), pya.Point(336, 8448)])
# polygon_id: p1287
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 251))).insert(p1287)
p1288 = pya.Polygon([pya.Point(12360, 4224), pya.Point(12360, 4320), pya.Point(12696, 4320), pya.Point(12696, 4224)])
# polygon_id: p1288
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 251))).insert(p1288)
p1289 = pya.Polygon([pya.Point(12360, 4608), pya.Point(12360, 4704), pya.Point(12696, 4704), pya.Point(12696, 4608)])
# polygon_id: p1289
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 251))).insert(p1289)
p1290 = pya.Polygon([pya.Point(12360, 3840), pya.Point(12360, 3936), pya.Point(12696, 3936), pya.Point(12696, 3840)])
# polygon_id: p1290
cell_Block3.shapes(layout.layer(pya.LayerInfo(40, 251))).insert(p1290)
p1299 = pya.Polygon([pya.Point(4992, 12360), pya.Point(4992, 12696), pya.Point(5088, 12696), pya.Point(5088, 12360)])
# polygon_id: p1299
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 251))).insert(p1299)
p1300 = pya.Polygon([pya.Point(5376, 12360), pya.Point(5376, 12696), pya.Point(5472, 12696), pya.Point(5472, 12360)])
# polygon_id: p1300
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 251))).insert(p1300)
p1301 = pya.Polygon([pya.Point(5376, 0), pya.Point(5376, 336), pya.Point(5472, 336), pya.Point(5472, 0)])
# polygon_id: p1301
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 251))).insert(p1301)
p1302 = pya.Polygon([pya.Point(7296, 0), pya.Point(7296, 336), pya.Point(7392, 336), pya.Point(7392, 0)])
# polygon_id: p1302
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 251))).insert(p1302)
p1303 = pya.Polygon([pya.Point(4608, 12360), pya.Point(4608, 12696), pya.Point(4704, 12696), pya.Point(4704, 12360)])
# polygon_id: p1303
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 251))).insert(p1303)
p1304 = pya.Polygon([pya.Point(5760, 12360), pya.Point(5760, 12696), pya.Point(5856, 12696), pya.Point(5856, 12360)])
# polygon_id: p1304
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 251))).insert(p1304)
p1305 = pya.Polygon([pya.Point(5760, 0), pya.Point(5760, 336), pya.Point(5856, 336), pya.Point(5856, 0)])
# polygon_id: p1305
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 251))).insert(p1305)
p1306 = pya.Polygon([pya.Point(7680, 0), pya.Point(7680, 336), pya.Point(7776, 336), pya.Point(7776, 0)])
# polygon_id: p1306
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 251))).insert(p1306)
p1307 = pya.Polygon([pya.Point(4224, 12360), pya.Point(4224, 12696), pya.Point(4320, 12696), pya.Point(4320, 12360)])
# polygon_id: p1307
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 251))).insert(p1307)
p1308 = pya.Polygon([pya.Point(6144, 12360), pya.Point(6144, 12696), pya.Point(6240, 12696), pya.Point(6240, 12360)])
# polygon_id: p1308
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 251))).insert(p1308)
p1309 = pya.Polygon([pya.Point(7296, 12360), pya.Point(7296, 12696), pya.Point(7392, 12696), pya.Point(7392, 12360)])
# polygon_id: p1309
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 251))).insert(p1309)
p1310 = pya.Polygon([pya.Point(6528, 0), pya.Point(6528, 336), pya.Point(6624, 336), pya.Point(6624, 0)])
# polygon_id: p1310
cell_Block3.shapes(layout.layer(pya.LayerInfo(50, 251))).insert(p1310)
# instance_id: i0001
cell_Block3.insert(pya.CellInstArray(cell_VIA_via1_2_2322_18_1_64_36_36.cell_index(), pya.Trans(0, False, pya.Vector(6372, 8640))))
# instance_id: i0002
cell_Block3.insert(pya.CellInstArray(cell_VIA_via1_2_2322_18_1_64_36_36.cell_index(), pya.Trans(0, False, pya.Vector(6372, 5400))))
# instance_id: i0003
cell_Block3.insert(pya.CellInstArray(cell_VIA_via1_2_2322_18_1_64_36_36.cell_index(), pya.Trans(0, False, pya.Vector(6372, 6480))))
# instance_id: i0004
cell_Block3.insert(pya.CellInstArray(cell_VIA_via1_2_2322_18_1_64_36_36.cell_index(), pya.Trans(0, False, pya.Vector(6372, 4320))))
# instance_id: i0005
cell_Block3.insert(pya.CellInstArray(cell_VIA_via1_2_2322_18_1_64_36_36.cell_index(), pya.Trans(0, False, pya.Vector(6372, 10800))))
# instance_id: i0006
cell_Block3.insert(pya.CellInstArray(cell_VIA_via1_2_2322_18_1_64_36_36.cell_index(), pya.Trans(0, False, pya.Vector(6372, 3240))))
# instance_id: i0007
cell_Block3.insert(pya.CellInstArray(cell_VIA_via1_2_2322_18_1_64_36_36.cell_index(), pya.Trans(0, False, pya.Vector(6372, 2160))))
# instance_id: i0008
cell_Block3.insert(pya.CellInstArray(cell_VIA_via1_2_2322_18_1_64_36_36.cell_index(), pya.Trans(0, False, pya.Vector(6372, 7560))))
# instance_id: i0009
cell_Block3.insert(pya.CellInstArray(cell_VIA_via1_2_2322_18_1_64_36_36.cell_index(), pya.Trans(0, False, pya.Vector(6372, 9720))))
# instance_id: i0010
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(6084, 9900))))
# instance_id: i0011
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(6120, 6660))))
# instance_id: i0012
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(9252, 6156))))
# instance_id: i0013
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(9396, 6156))))
# instance_id: i0014
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(2484, 6156))))
# instance_id: i0015
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6804, 6156))))
# instance_id: i0016
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(6948, 9900))))
# instance_id: i0017
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(7956, 10620))))
# instance_id: i0018
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(7524, 10044))))
# instance_id: i0019
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(9108, 10620))))
# instance_id: i0020
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(8532, 10044))))
# instance_id: i0021
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(9972, 9900))))
# instance_id: i0022
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(9396, 6660))))
# instance_id: i0023
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(7380, 9540))))
# instance_id: i0024
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(8388, 6300))))
# instance_id: i0025
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(7236, 7380))))
# instance_id: i0026
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(10260, 6660))))
# instance_id: i0027
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(8532, 9540))))
# instance_id: i0028
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(8964, 8820))))
# instance_id: i0029
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(6372, 10476))))
# instance_id: i0030
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(8964, 6660))))
# instance_id: i0031
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(6804, 7380))))
# instance_id: i0032
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(9612, 10332))))
# instance_id: i0033
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(8280, 7380))))
# instance_id: i0034
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(7956, 7740))))
# instance_id: i0035
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(9252, 7884))))
# instance_id: i0036
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(7956, 7380))))
# instance_id: i0037
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(9108, 10620))))
# instance_id: i0038
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6948, 9900))))
# instance_id: i0039
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7956, 10620))))
# instance_id: i0040
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7956, 10980))))
# instance_id: i0041
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(7092, 6300))))
# instance_id: i0042
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(8964, 8820))))
# instance_id: i0043
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(9828, 6948))))
# instance_id: i0044
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(9252, 7884))))
# instance_id: i0045
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(9252, 7380))))
# instance_id: i0046
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(9396, 6660))))
# instance_id: i0047
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(9684, 7740))))
# instance_id: i0048
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(10260, 6660))))
# instance_id: i0049
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6372, 10476))))
# instance_id: i0050
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7380, 8028))))
# instance_id: i0051
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(10116, 9396))))
# instance_id: i0052
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(8676, 6660))))
# instance_id: i0053
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6660, 7380))))
# instance_id: i0054
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6660, 8316))))
# instance_id: i0055
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7956, 7380))))
# instance_id: i0056
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7956, 7740))))
# instance_id: i0057
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7524, 8964))))
# instance_id: i0058
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7524, 10332))))
# instance_id: i0059
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7812, 8820))))
# instance_id: i0060
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7092, 6660))))
# instance_id: i0061
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7092, 8172))))
# instance_id: i0062
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7236, 7380))))
# instance_id: i0063
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7236, 9252))))
# instance_id: i0064
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(9684, 7740))))
# instance_id: i0065
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6516, 9900))))
# instance_id: i0066
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6372, 7884))))
# instance_id: i0067
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7380, 9108))))
# instance_id: i0068
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7380, 8820))))
# instance_id: i0069
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7668, 10044))))
# instance_id: i0070
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(9972, 9900))))
# instance_id: i0071
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(8532, 10044))))
# instance_id: i0072
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(6372, 10992))))
# instance_id: i0073
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(9108, 10800))))
# instance_id: i0074
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(10260, 6576))))
# instance_id: i0075
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45.cell_index(), pya.Trans(0, False, pya.Vector(6192, 9648))))
# instance_id: i0076
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45.cell_index(), pya.Trans(0, False, pya.Vector(7344, 10800))))
# instance_id: i0077
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4212, 10980))))
# instance_id: i0078
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45_1_2_58_58.cell_index(), pya.Trans(0, False, pya.Vector(2128, 8640))))
# instance_id: i0079
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45_1_2_58_58.cell_index(), pya.Trans(0, False, pya.Vector(2128, 6480))))
# instance_id: i0080
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(4212, 9900))))
# instance_id: i0081
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(2484, 7380))))
# instance_id: i0082
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(5220, 9540))))
# instance_id: i0083
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45_1_2_58_58.cell_index(), pya.Trans(0, False, pya.Vector(2896, 7560))))
# instance_id: i0084
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4356, 10620))))
# instance_id: i0085
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45_1_2_58_58.cell_index(), pya.Trans(0, False, pya.Vector(2896, 9720))))
# instance_id: i0086
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(4500, 8964))))
# instance_id: i0087
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4644, 6948))))
# instance_id: i0088
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34_1_2_58_52.cell_index(), pya.Trans(0, False, pya.Vector(2896, 9720))))
# instance_id: i0089
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(5508, 6660))))
# instance_id: i0090
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34_1_2_58_52.cell_index(), pya.Trans(0, False, pya.Vector(2128, 10800))))
# instance_id: i0091
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4788, 9900))))
# instance_id: i0092
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(1332, 8460))))
# instance_id: i0093
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(5364, 10476))))
# instance_id: i0094
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(1620, 7092))))
# instance_id: i0095
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(3060, 10476))))
# instance_id: i0096
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34_1_2_58_52.cell_index(), pya.Trans(0, False, pya.Vector(2896, 7560))))
# instance_id: i0097
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(3348, 10476))))
# instance_id: i0098
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(3348, 8820))))
# instance_id: i0099
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(3060, 7380))))
# instance_id: i0100
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(3348, 7092))))
# instance_id: i0101
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34_1_2_58_52.cell_index(), pya.Trans(0, False, pya.Vector(2128, 8640))))
# instance_id: i0102
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34_1_2_58_52.cell_index(), pya.Trans(0, False, pya.Vector(2128, 6480))))
# instance_id: i0103
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(5220, 7740))))
# instance_id: i0104
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(2268, 9252))))
# instance_id: i0105
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(3348, 10476))))
# instance_id: i0106
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(4788, 9900))))
# instance_id: i0107
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(5364, 10476))))
# instance_id: i0108
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(3780, 7380))))
# instance_id: i0109
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23_1_3_36_36.cell_index(), pya.Trans(0, False, pya.Vector(2128, 10800))))
# instance_id: i0110
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23_1_3_36_36.cell_index(), pya.Trans(0, False, pya.Vector(2128, 8640))))
# instance_id: i0111
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(2340, 10476))))
# instance_id: i0112
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23_1_3_36_36.cell_index(), pya.Trans(0, False, pya.Vector(2128, 6480))))
# instance_id: i0113
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(5364, 6660))))
# instance_id: i0114
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(1188, 9252))))
# instance_id: i0115
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(2340, 7380))))
# instance_id: i0116
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23_1_3_36_36.cell_index(), pya.Trans(0, False, pya.Vector(2896, 7560))))
# instance_id: i0117
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(5220, 7740))))
# instance_id: i0118
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(3348, 8820))))
# instance_id: i0119
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(4500, 10620))))
# instance_id: i0120
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(2268, 8460))))
# instance_id: i0121
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4500, 8964))))
# instance_id: i0122
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23_1_3_36_36.cell_index(), pya.Trans(0, False, pya.Vector(2896, 9720))))
# instance_id: i0123
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4212, 9900))))
# instance_id: i0124
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(3960, 6660))))
# instance_id: i0125
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(5364, 11376))))
# instance_id: i0126
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(1332, 8496))))
# instance_id: i0127
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(3924, 6660))))
# instance_id: i0128
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(5220, 9648))))
# instance_id: i0129
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(1188, 9264))))
# instance_id: i0130
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(3348, 10608))))
# instance_id: i0131
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(4212, 11184))))
# instance_id: i0132
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(1620, 8880))))
# instance_id: i0133
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(5220, 9540))))
# instance_id: i0134
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(3060, 11376))))
# instance_id: i0135
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(3492, 9900))))
# instance_id: i0136
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45.cell_index(), pya.Trans(0, False, pya.Vector(4272, 11184))))
# instance_id: i0137
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45.cell_index(), pya.Trans(0, False, pya.Vector(5040, 10608))))
# instance_id: i0138
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(3060, 9900))))
# instance_id: i0139
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45.cell_index(), pya.Trans(0, False, pya.Vector(5424, 11376))))
# instance_id: i0140
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45_1_2_58_58.cell_index(), pya.Trans(0, False, pya.Vector(2128, 10800))))
# instance_id: i0141
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45.cell_index(), pya.Trans(0, False, pya.Vector(3696, 6576))))
# instance_id: i0142
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45.cell_index(), pya.Trans(0, False, pya.Vector(4656, 11376))))
# instance_id: i0143
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45.cell_index(), pya.Trans(0, False, pya.Vector(5808, 10992))))
# instance_id: i0144
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34_1_2_58_52.cell_index(), pya.Trans(0, False, pya.Vector(2128, 2160))))
# instance_id: i0145
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(2916, 4932))))
# instance_id: i0146
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(3348, 2916))))
# instance_id: i0147
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45_1_2_58_58.cell_index(), pya.Trans(0, False, pya.Vector(2896, 5400))))
# instance_id: i0148
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4932, 5220))))
# instance_id: i0149
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(3780, 5220))))
# instance_id: i0150
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4356, 5580))))
# instance_id: i0151
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34_1_2_58_52.cell_index(), pya.Trans(0, False, pya.Vector(2896, 3240))))
# instance_id: i0152
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34_1_2_58_52.cell_index(), pya.Trans(0, False, pya.Vector(2128, 4320))))
# instance_id: i0153
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(4212, 3060))))
# instance_id: i0154
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4356, 2916))))
# instance_id: i0155
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4068, 4500))))
# instance_id: i0156
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4212, 3564))))
# instance_id: i0157
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4068, 3996))))
# instance_id: i0158
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4644, 4140))))
# instance_id: i0159
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4356, 4500))))
# instance_id: i0160
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(5220, 4500))))
# instance_id: i0161
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(5220, 5076))))
# instance_id: i0162
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23_1_3_36_36.cell_index(), pya.Trans(0, False, pya.Vector(2896, 3240))))
# instance_id: i0163
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45_1_2_58_58.cell_index(), pya.Trans(0, False, pya.Vector(2128, 2160))))
# instance_id: i0164
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(4500, 4140))))
# instance_id: i0165
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(5220, 5868))))
# instance_id: i0166
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(5508, 4644))))
# instance_id: i0167
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4500, 3060))))
# instance_id: i0168
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(5508, 3060))))
# instance_id: i0169
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(3924, 5220))))
# instance_id: i0170
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(3636, 2484))))
# instance_id: i0171
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(4068, 4500))))
# instance_id: i0172
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4788, 4932))))
# instance_id: i0173
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45_1_2_58_58.cell_index(), pya.Trans(0, False, pya.Vector(2896, 3240))))
# instance_id: i0174
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(4644, 2484))))
# instance_id: i0175
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(5220, 2772))))
# instance_id: i0176
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(4932, 5232))))
# instance_id: i0177
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45_1_2_58_58.cell_index(), pya.Trans(0, False, pya.Vector(2128, 4320))))
# instance_id: i0178
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(4068, 5580))))
# instance_id: i0179
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(4788, 5220))))
# instance_id: i0180
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(4644, 2484))))
# instance_id: i0181
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(5724, 2628))))
# instance_id: i0182
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(5220, 1200))))
# instance_id: i0183
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(4644, 1008))))
# instance_id: i0184
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(3636, 2544))))
# instance_id: i0185
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(3924, 5424))))
# instance_id: i0186
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(3348, 5724))))
# instance_id: i0187
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23_1_3_36_36.cell_index(), pya.Trans(0, False, pya.Vector(2128, 4320))))
# instance_id: i0188
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23_1_3_36_36.cell_index(), pya.Trans(0, False, pya.Vector(2896, 5400))))
# instance_id: i0189
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(3492, 3708))))
# instance_id: i0190
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(3780, 3852))))
# instance_id: i0191
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45.cell_index(), pya.Trans(0, False, pya.Vector(5808, 1008))))
# instance_id: i0192
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34_1_2_58_52.cell_index(), pya.Trans(0, False, pya.Vector(2896, 5400))))
# instance_id: i0193
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45.cell_index(), pya.Trans(0, False, pya.Vector(5424, 1200))))
# instance_id: i0194
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23_1_3_36_36.cell_index(), pya.Trans(0, False, pya.Vector(2128, 2160))))
# instance_id: i0195
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45.cell_index(), pya.Trans(0, False, pya.Vector(3696, 2544))))
# instance_id: i0196
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(2484, 2772))))
# instance_id: i0197
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(3924, 6012))))
# instance_id: i0198
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(3636, 2484))))
# instance_id: i0199
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(8388, 4932))))
# instance_id: i0200
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(9108, 4932))))
# instance_id: i0201
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(9108, 5580))))
# instance_id: i0202
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(9684, 5076))))
# instance_id: i0203
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(10404, 4140))))
# instance_id: i0204
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(8388, 3564))))
# instance_id: i0205
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(10116, 3060))))
# instance_id: i0206
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6516, 5724))))
# instance_id: i0207
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(9684, 2916))))
# instance_id: i0208
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6516, 2628))))
# instance_id: i0209
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7236, 3996))))
# instance_id: i0210
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(8676, 5580))))
# instance_id: i0211
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6372, 2340))))
# instance_id: i0212
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(6804, 2484))))
# instance_id: i0213
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(8964, 3852))))
# instance_id: i0214
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(6660, 4500))))
# instance_id: i0215
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7812, 4140))))
# instance_id: i0216
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6804, 2484))))
# instance_id: i0217
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(9684, 2916))))
# instance_id: i0218
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(8532, 5220))))
# instance_id: i0219
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(6228, 3420))))
# instance_id: i0220
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(9108, 4140))))
# instance_id: i0221
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(7812, 4140))))
# instance_id: i0222
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(9396, 3852))))
# instance_id: i0223
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6516, 3060))))
# instance_id: i0224
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(9972, 3564))))
# instance_id: i0225
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6516, 4932))))
# instance_id: i0226
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(6228, 5232))))
# instance_id: i0227
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(7380, 3060))))
# instance_id: i0228
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(10404, 3888))))
# instance_id: i0229
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(9684, 3504))))
# instance_id: i0230
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(8100, 5076))))
# instance_id: i0231
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(7236, 3996))))
# instance_id: i0232
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(10116, 3060))))
# instance_id: i0233
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(7380, 3060))))
# instance_id: i0234
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(6804, 1200))))
# instance_id: i0235
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(10404, 4656))))
# instance_id: i0236
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(8676, 4500))))
# instance_id: i0237
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(6660, 4140))))
# instance_id: i0238
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(9684, 5076))))
# instance_id: i0239
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(9684, 5580))))
# instance_id: i0240
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(9108, 4272))))
# instance_id: i0241
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(9108, 4140))))
# instance_id: i0242
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(8388, 2340))))
# instance_id: i0243
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(7668, 5424))))
# instance_id: i0244
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6804, 3420))))
# instance_id: i0245
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(8100, 5580))))
# instance_id: i0246
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(8388, 2340))))
# instance_id: i0247
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(8100, 5076))))
# instance_id: i0248
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(6516, 2160))))
# instance_id: i0249
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(8388, 1008))))
# instance_id: i0250
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA34.cell_index(), pya.Trans(0, False, pya.Vector(7236, 5040))))
# instance_id: i0251
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(7956, 2916))))
# instance_id: i0252
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6228, 6012))))
# instance_id: i0253
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6660, 4140))))
# instance_id: i0254
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45.cell_index(), pya.Trans(0, False, pya.Vector(7728, 1200))))
# instance_id: i0255
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6660, 4788))))
# instance_id: i0256
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(10404, 4500))))
# instance_id: i0257
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(6372, 2340))))
# instance_id: i0258
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(10404, 4140))))
# instance_id: i0259
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45.cell_index(), pya.Trans(0, False, pya.Vector(7344, 2160))))
# instance_id: i0260
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(6948, 5868))))
# instance_id: i0261
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(10404, 4500))))
# instance_id: i0262
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA45.cell_index(), pya.Trans(0, False, pya.Vector(6576, 1008))))
# instance_id: i0263
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA12.cell_index(), pya.Trans(0, False, pya.Vector(8676, 5220))))
# instance_id: i0264
cell_Block3.insert(pya.CellInstArray(cell_VIA_VIA23.cell_index(), pya.Trans(0, False, pya.Vector(8388, 2916))))
# instance_id: i0265
cell_Block3.insert(pya.CellInstArray(cell_FILLERxp5_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(2160, 2160))))
# instance_id: i0266
cell_Block3.insert(pya.CellInstArray(cell_FILLERxp5_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(8640, 6480))))
# instance_id: i0267
cell_Block3.insert(pya.CellInstArray(cell_FILLERxp5_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(4968, 6480))))
# instance_id: i0268
cell_Block3.insert(pya.CellInstArray(cell_FILLERxp5_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(2592, 4320))))
# instance_id: i0269
cell_Block3.insert(pya.CellInstArray(cell_FILLERxp5_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(9288, 2160))))
# instance_id: i0270
cell_Block3.insert(pya.CellInstArray(cell_FILLERxp5_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(2592, 4320))))
# instance_id: i0271
cell_Block3.insert(pya.CellInstArray(cell_FILLERxp5_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(10368, 10800))))
# instance_id: i0272
cell_Block3.insert(pya.CellInstArray(cell_FILLERxp5_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(5832, 4320))))
# instance_id: i0273
cell_Block3.insert(pya.CellInstArray(cell_FILLER_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(2160, 4320))))
# instance_id: i0274
cell_Block3.insert(pya.CellInstArray(cell_FILLER_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(9072, 4320))))
# instance_id: i0275
cell_Block3.insert(pya.CellInstArray(cell_FILLER_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(4536, 6480))))
# instance_id: i0276
cell_Block3.insert(pya.CellInstArray(cell_FILLER_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(8856, 2160))))
# instance_id: i0277
cell_Block3.insert(pya.CellInstArray(cell_FILLER_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(6264, 6480))))
# instance_id: i0278
cell_Block3.insert(pya.CellInstArray(cell_FILLER_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(2160, 4320))))
# instance_id: i0279
cell_Block3.insert(pya.CellInstArray(cell_FILLER_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(10152, 6480))))
# instance_id: i0280
cell_Block3.insert(pya.CellInstArray(cell_FILLER_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(10152, 8640))))
# instance_id: i0281
cell_Block3.insert(pya.CellInstArray(cell_DECAPx2_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(9288, 8640))))
# instance_id: i0282
cell_Block3.insert(pya.CellInstArray(cell_TAPCELL_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(1728, 2160))))
# instance_id: i0283
cell_Block3.insert(pya.CellInstArray(cell_TAPCELL_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(1728, 4320))))
# instance_id: i0284
cell_Block3.insert(pya.CellInstArray(cell_TAPCELL_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(1728, 8640))))
# instance_id: i0285
cell_Block3.insert(pya.CellInstArray(cell_TAPCELL_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(1728, 6480))))
# instance_id: i0286
cell_Block3.insert(pya.CellInstArray(cell_TAPCELL_ASAP7_75t_R.cell_index(), pya.Trans(2, False, pya.Vector(11016, 10800))))
# instance_id: i0287
cell_Block3.insert(pya.CellInstArray(cell_TAPCELL_ASAP7_75t_R.cell_index(), pya.Trans(2, False, pya.Vector(11016, 4320))))
# instance_id: i0288
cell_Block3.insert(pya.CellInstArray(cell_TAPCELL_ASAP7_75t_R.cell_index(), pya.Trans(2, False, pya.Vector(11016, 8640))))
# instance_id: i0289
cell_Block3.insert(pya.CellInstArray(cell_TAPCELL_ASAP7_75t_R.cell_index(), pya.Trans(2, False, pya.Vector(11016, 6480))))
# instance_id: i0290
cell_Block3.insert(pya.CellInstArray(cell_TAPCELL_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(1728, 4320))))
# instance_id: i0291
cell_Block3.insert(pya.CellInstArray(cell_TAPCELL_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(1728, 10800))))
# instance_id: i0292
cell_Block3.insert(pya.CellInstArray(cell_TAPCELL_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(1728, 8640))))
# instance_id: i0293
cell_Block3.insert(pya.CellInstArray(cell_TAPCELL_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(1728, 6480))))
# instance_id: i0294
cell_Block3.insert(pya.CellInstArray(cell_TAPCELL_ASAP7_75t_R.cell_index(), pya.Trans(6, True, pya.Vector(11016, 6480))))
# instance_id: i0295
cell_Block3.insert(pya.CellInstArray(cell_TAPCELL_ASAP7_75t_R.cell_index(), pya.Trans(6, True, pya.Vector(11016, 4320))))
# instance_id: i0296
cell_Block3.insert(pya.CellInstArray(cell_TAPCELL_ASAP7_75t_R.cell_index(), pya.Trans(6, True, pya.Vector(11016, 8640))))
# instance_id: i0297
cell_Block3.insert(pya.CellInstArray(cell_TAPCELL_ASAP7_75t_R.cell_index(), pya.Trans(6, True, pya.Vector(11016, 2160))))
# instance_id: i0298
cell_Block3.insert(pya.CellInstArray(cell_INVx3_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(2160, 6480))))
# instance_id: i0299
cell_Block3.insert(pya.CellInstArray(cell_INVx3_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(3888, 4320))))
# instance_id: i0300
cell_Block3.insert(pya.CellInstArray(cell_INVx3_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(6696, 6480))))
# instance_id: i0301
cell_Block3.insert(pya.CellInstArray(cell_INVx3_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(5184, 6480))))
# instance_id: i0302
cell_Block3.insert(pya.CellInstArray(cell_INVx3_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(6048, 4320))))
# instance_id: i0303
cell_Block3.insert(pya.CellInstArray(cell_INVx2_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(8856, 6480))))
# instance_id: i0304
cell_Block3.insert(pya.CellInstArray(cell_INVx2_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(9720, 6480))))
# instance_id: i0305
cell_Block3.insert(pya.CellInstArray(cell_INVx2_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(7776, 6480))))
# instance_id: i0306
cell_Block3.insert(pya.CellInstArray(cell_INVx2_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(8424, 8640))))
# instance_id: i0307
cell_Block3.insert(pya.CellInstArray(cell_INVx2_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(9504, 10800))))
# instance_id: i0308
cell_Block3.insert(pya.CellInstArray(cell_INVx2_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(8208, 6480))))
# instance_id: i0309
cell_Block3.insert(pya.CellInstArray(cell_INVx2_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(4320, 10800))))
# instance_id: i0310
cell_Block3.insert(pya.CellInstArray(cell_FAx1_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(4968, 4320))))
# instance_id: i0311
cell_Block3.insert(pya.CellInstArray(cell_FAx1_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(5400, 8640))))
# instance_id: i0312
cell_Block3.insert(pya.CellInstArray(cell_FAx1_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(2808, 4320))))
# instance_id: i0313
cell_Block3.insert(pya.CellInstArray(cell_FAx1_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(5184, 6480))))
# instance_id: i0314
cell_Block3.insert(pya.CellInstArray(cell_FAx1_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(6048, 8640))))
# instance_id: i0315
cell_Block3.insert(pya.CellInstArray(cell_FAx1_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(2160, 6480))))
# instance_id: i0316
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(2376, 2160))))
# instance_id: i0317
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(4320, 8640))))
# instance_id: i0318
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(7992, 4320))))
# instance_id: i0319
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(9504, 2160))))
# instance_id: i0320
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(5616, 2160))))
# instance_id: i0321
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(6696, 2160))))
# instance_id: i0322
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(4536, 2160))))
# instance_id: i0323
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(7776, 2160))))
# instance_id: i0324
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(3456, 2160))))
# instance_id: i0325
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(2808, 4320))))
# instance_id: i0326
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(9504, 4320))))
# instance_id: i0327
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(8208, 4320))))
# instance_id: i0328
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(7128, 4320))))
# instance_id: i0329
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(6264, 10800))))
# instance_id: i0330
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(2160, 10800))))
# instance_id: i0331
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(7344, 10800))))
# instance_id: i0332
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(5184, 10800))))
# instance_id: i0333
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(3240, 10800))))
# instance_id: i0334
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(8424, 10800))))
# instance_id: i0335
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(9072, 8640))))
# instance_id: i0336
cell_Block3.insert(pya.CellInstArray(cell_BUFx2_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(9072, 6480))))
# instance_id: i0337
cell_Block3.insert(pya.CellInstArray(cell_BUFx6f_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(2160, 8640))))
# instance_id: i0338
cell_Block3.insert(pya.CellInstArray(cell_BUFx12f_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(2160, 8640))))
# instance_id: i0339
cell_Block3.insert(pya.CellInstArray(cell_BUFx3_ASAP7_75t_R.cell_index(), pya.Trans(0, False, pya.Vector(3240, 6480))))
# instance_id: i0340
cell_Block3.insert(pya.CellInstArray(cell_BUFx3_ASAP7_75t_R.cell_index(), pya.Trans(4, True, pya.Vector(9288, 4320))))

layout.write("../gds/Block3.gds")
