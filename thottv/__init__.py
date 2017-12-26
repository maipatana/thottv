"""
Thailand OTTV Calculation module
Developed by Patana Rattananvathong 18-Dec-2017
========================
This library was designed for calculting OTTV, RTTV and WBC
to meet the Thailand Building Code for the Building Energy Conservation.
The Code was introduced by the Ministry of Energy, Thailand in 2009.
"""

import os

class con:
    def __init__(self, name="Construction"):
        self.name = name
        self.materials = []
        self.material_thickness = []
        self.material_conductivity = []
        self.material_density = []
        self.material_heat_capacity = []
        self.r_value = 0
        self.u_value = 0
        self.dsh = 0

    def uvalue(self):
        self.r_value = 0.12+0.044+sum([t/k for t,k in zip(
                    self.material_thickness,self.material_conductivity )])
        self.u_value = 1/self.r_value if self.r_value!=0 else 0
        self.dsh = sum([t*r*cp for t,r,cp in zip(
                    self.material_thickness, self.material_density,
                    self.material_heat_capacity)])

    def add_mat(self,material,thickness, conductivity, density, specificheatcapacity):
        self.materials.append(material)
        self.material_thickness.append(thickness)
        self.material_conductivity.append(conductivity)
        self.material_density.append(density)
        self.material_heat_capacity.append(specificheatcapacity)
        self.uvalue()

    def section(self):
        totalthickness = 0
        for name,t,k in zip(self.materials,self.material_thickness,self.material_conductivity):
            totalthickness+=t
            print("Name:{} Thickness:{} Conductivity:{}".format(name,t,k))
        print("Total Thinkness: {:.2f}m".format(totalthickness))

    def remove_mat(self,nameorindex):
        if isinstance(nameorindex,int):
            if nameorindex > len(self.materials)-1:
                return "The index is out of range."
            index = nameorindex
        else:
            if nameorindex not in self.materials:
                return "There is no selected material."
            else:
                index = self.materials.index(nameorindex)

        self.materials.pop(index)
        self.material_conductivity.pop(index)
        self.material_thickness.pop(index)
        self.material_density.pop(index)
        self.material_heat_capacity.pop(index)
        self.uvalue()

    def clear(self):
        self.materials = []
        self.material_thickness = []
        self.material_conductivity = []
        self.material_density = []
        self.material_heat_capacity = []
        self.uvalue()

class wall:
    def __init__(self, name="Wall", orientation = 0, tilt = 90):
        self.name = name
        self.orientation = orientation
        self.tile = tilt
        self.conlist = []
        self.colorlist = []
        self.arealist = []
        self.tdeq = []

        self.TDEQ_LIST = {"office":{180:{15:[12.5,17.2,21.9,26.6],
                               30:[12.1,16.7,21.3,25.9],
                               50:[11.6,16.0,20.5,25.9],
                               100:[10.5,14.6,18.8,23.0],
                               200:[7.9,10.6,13.4,16.1],
                               300:[7.3,9.9,12.5,15.1],
                               400:[7.1,9.6,12.2,14.7]},
                          270:{15:[12.6,17.2,21.9,26.5],
                               30:[12.3,16.9,21.5,26.1],
                               50:[11.9,16.5,21.1,25.6],
                               100:[11.1,15.5,20.0,24.4],
                               200:[9.8,13.9,18.0,22.2],
                               300:[9.0,12.8,16.6,20.4],
                               400:[8.6,12.2,15.8,19.4]},
                          0:{15:[13.0,18.0,22.9,27.8],
                               30:[12.7,17.5,22.3,27.1],
                               50:[12.2,16.9,21.6,26.3],
                               100:[11.1,15.6,20.1,24.6],
                               200:[9.7,13.7,17.8,21.9],
                               300:[8.9,12.7,15.9,19.5],
                               400:[8.6,12.2,15.9,19.5]},
                          90:{15:[12.3,16.7,21.1,25.5],
                               30:[11.9,16.2,20.4,24.7],
                               50:[11.3,15.5,19.6,23.7],
                               100:[10.2,14.0,17.8,21.6],
                               200:[8.7,12.1,15.5,18.9],
                               300:[8.1,11.2,14.4,17.6],
                               400:[7.9,11.0,14.1,17.6]}
                                   }
                         }

    def add_con(self, obj, area,color=0.3):
        self.conlist.append(obj)
        self.arealist.append(area)
        self.colorlist.append(color)
        self.get_tdeq()

    def set_ori(self, orientation):
        self.orientation = orientation
        self.get_tdeq()

    def set_tilt(self, tilt):
        self.tilt = tilt
        self.get_tdeq()

    def get_tdeq(self):
        col = {0.3:0,0.5:1,0.7:2,0.9:3}
        self.tdeq = []
        for con,color in zip(self.conlist,self.colorlist):
            neardsh = min([15,30,50,100,200,300,400], key=lambda x:abs(x-con.dsh))
            self.tdeq.append(self.TDEQ_LIST["office"][self.orientation][neardsh][col[color]])

    def clear(self):
        self.conlist = []
        self.colorlist = []
        self.arealist = []
        self.tdeq = []


class space:
    def __init__(self,name="Space",area=0,spacetype=None):
        self.name = name
        self.area = area
        self.space_type = spacetype
        self.walls = []
        self.total_wall_area = 0
        self.total_q = 0
        self.ottv = 0

    def clear_wall(self):
        self.walls=[]
        self.update()

    def add_wall(self, obj):
        self.walls.append(obj)
        self.update()

    def get_ottv(self):
        self.update()
        return self.ottv

    def get_rttv(self):
        return 1

    def get_wbc(self):
        return 1

    def set_lsd(self, lighting):
        self.lsd = lighting

    def set_area(self, area):
        self.area = area

    def set_cop(self, cop):
        self.cop = cop

    def set_type(self, spacetype):
        self.space_type = spacetype

    def update(self):
        self.total_wall_area = 0
        self.total_q = 0
        for wall in self.walls:
            self.total_wall_area+=sum(wall.arealist)
            self.total_q+= sum([u.u_value*area*tdeq for u,area,tdeq in zip(wall.conlist,wall.arealist,wall.tdeq)])
        self.ottv = self.total_q/self.total_wall_area

    def __walls__(self):
        print("List of Walls:")
        for wall in self.walls:
            con = ["{} u_value:{:.2f}".format(con.name,con.u_value) for con in wall.conlist]
            print(wall.name,con)
