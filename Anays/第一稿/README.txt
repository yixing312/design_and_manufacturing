by zsb ver1

1、建模导入的是zhgg的ver2版本，整体仿真参数设置过程与PPT一致

2、命名选择中，各螺栓序号与sw文件中螺栓序号一致，为7-12。用到命名选择的面有：各螺栓下表面(boltx_down)、上法兰上表面(up_up)、各螺栓
螺纹面(bolt_x)、下法兰螺纹孔内表面(down_x)、上法兰扇面(up_X)、下法兰扇面(down_X)

3、目前仿真求解项有整体总变形，以及自定义的一个截面上x方向变形量，还不能得到同轴度

4、子部件id：
bolt11 	209
bolt8  	211
bolt9	213
bolt10	215
bolt7	217
bolt12	219
获取方法：示教

5、自动化：利用文件中的calculate.py脚本，保存的结果路径为：ansys_1_files/user_files/


by the way ANSYS参数设置真麻烦啊啊啊啊啊啊