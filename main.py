import requests
import re
import time

listOfParam = ['Час по местному времени', 'День.Месяц.Год', 'Направление ветра', 'V ветра, м/с', 't воздуха, `C', 'Влажность, %',
                'Давление воздуха на высоте места измерения над уровнем моря, мм рт. ст.', 'min t воздуха, `C', 'max t воздуха, `C',
                'Количество осадков за последние 12ч, мм', 'Высота снежного покрова, см', 'Состояние снега, величина покрытия местности в баллах']

# Для быстрой отладки:
t = '''</tr>

    <tr height="30" bgColor=#ffffff>
    <td class=black><b>00</b></td>
    <td class=black><b>1.12</b></td>
    <td class="wind_w">З</td>
    <td class="ff_3">3</td>
    <td class="vis_2">20 км</td>
    <td class="w_"> <i>{ливн. осадки}</i></td>
    <td class="vis_8">8/8 600 м<br>[Cb cap]</td>
    <td class="temp_30"><nobr>-21.0</nobr></td>
    <td class="temp_29"><nobr>-24.7</nobr></td>
    <td class="temp_38">72</td>
    <td class="temp_27"><nobr>-29</nobr></td>
    <td class="temp_27"><nobr>-29</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_37">1026.4</td>
    <td class="black">1009.8</td>
    <td class="temp_30"><nobr>-21.0</nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="за 12 ч." class="temp_39">1</td>
    <td class="temp_"></td>
    <td title="сухой снег 10 баллов" class="snow_9">36</td>
    </tr>
    <tr height="30" bgColor=#daf1f7>
    <td class=black><b>03</b></td>
    <td class=black><b>1.12</b></td>
    <td class="wind_sw">ЮЗ</td>
    <td class="ff_2">2</td>
    <td class="vis_3">10 км</td>
    <td class="w_sn">слаб. снег</td>
    <td class="vis_10">10 баллов</td>
    <td class="temp_30"><nobr>-22.1</nobr></td>
    <td class="temp_28"><nobr>-25.8</nobr></td>
    <td class="temp_38">72</td>
    <td class="temp_28"><nobr>-28</nobr></td>
    <td class="temp_28"><nobr>-28</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_36">1031.9</td>
    <td class="black">1014.7</td>
    <td class="temp_30"><nobr>-22.1</nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#ffffff>
    <td class=black><b>06</b></td>
    <td class=black><b>1.12</b></td>
    <td class="wind_sw">ЮЗ</td>
    <td class="ff_3">3</td>
    <td class="vis_2">20 км</td>
    <td class="w_"> <i>{снег}</i></td>
    <td class="vis_10">10/0<br>[As trans]</td>
    <td class="temp_30"><nobr>-21.7</nobr></td>
    <td class="temp_28"><nobr>-25.9</nobr></td>
    <td class="temp_38">69</td>
    <td class="temp_27"><nobr>-30</nobr></td>
    <td class="temp_27"><nobr>-29</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_35">1033.1</td>
    <td class="black">1016.3</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#daf1f7>
    <td class=black><b>09</b></td>
    <td class=black><b>1.12</b></td>
    <td class="wind_sw">ЮЗ</td>
    <td class="ff_2">2</td>
    <td class="vis_3">10 км</td>
    <td class="w_sn">слаб. снег</td>
    <td class="vis_10">10/0<br>[As op]</td>
    <td class="temp_30"><nobr>-20.4</nobr></td>
    <td class="temp_29"><nobr>-23.9</nobr></td>
    <td class="temp_38">73</td>
    <td class="temp_28"><nobr>-26</nobr></td>
    <td class="temp_28"><nobr>-26</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_35">1034.2</td>
    <td class="black">1017.5</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#ffffff>
    <td class=black><b>12</b></td>
    <td class=black><b>1.12</b></td>
    <td class="wind_s">Ю</td>
    <td class="ff_6">6</td>
    <td class="vis_3">10 км</td>
    <td class="w_sn">слаб. снег</td>
    <td class="vis_10">10/0<br>[As op]</td>
    <td class="temp_30"><nobr>-19.9</nobr></td>
    <td class="temp_29"><nobr>-22.7</nobr></td>
    <td class="temp_37">78</td>
    <td class="temp_27"><nobr>-31</nobr></td>
    <td class="temp_27"><nobr>-31</nobr></td>
    <td class="black" bgcolor="#9600FE">опасность<br> обморожения</td>
    <td class="temp_35">1035.7</td>
    <td class="black">1019.0</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_30"><nobr>-19.9</nobr></td>
    <td title="за 12 ч." class="temp_39">0.5</td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#daf1f7>
    <td class=black><b>15</b></td>
    <td class=black><b>1.12</b></td>
    <td class="wind_s">Ю</td>
    <td class="ff_3">3</td>
    <td class="vis_2">20 км</td>
    <td class="w_sn">слаб. снег</td>
    <td class="vis_10">10/0<br>[As op]</td>
    <td class="temp_31"><nobr>-18.9</nobr></td>
    <td class="temp_30"><nobr>-21.5</nobr></td>
    <td class="temp_37">80</td>
    <td class="temp_28"><nobr>-26</nobr></td>
    <td class="temp_28"><nobr>-26</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_35">1036.0</td>
    <td class="black">1019.3</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#ffffff>
    <td class=black><b>18</b></td>
    <td class=black><b>1.12</b></td>
    <td class="wind_se">ЮВ</td>
    <td class="ff_1">1</td>
    <td class="vis_2">20 км</td>
    <td class="w_sn">слаб. снег</td>
    <td class="vis_10">10/0<br>[As op]</td>
    <td class="temp_31"><nobr>-19.5</nobr></td>
    <td class="temp_30"><nobr>-21.8</nobr></td>
    <td class="temp_37">82</td>
    <td class="temp_30"><nobr>-22</nobr></td>
    <td class="temp_30"><nobr>-22</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_35">1036.3</td>
    <td class="black">1019.6</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#daf1f7>
    <td class=black><b>21</b></td>
    <td class=black><b>1.12</b></td>
    <td class="wind_s">Ю</td>
    <td class="ff_1">1</td>
    <td class="vis_2">20 км</td>
    <td class="w_sn">слаб. снег</td>
    <td class="vis_10">10/0<br>[As op]</td>
    <td class="temp_30"><nobr>-21.2</nobr></td>
    <td class="temp_29"><nobr>-23.4</nobr></td>
    <td class="temp_37">82</td>
    <td class="temp_29"><nobr>-24</nobr></td>
    <td class="temp_29"><nobr>-24</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_35">1036.9</td>
    <td class="black">1020.1</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#ffffff>
    <td class=black><b>00</b></td>
    <td class=black><b>2.12</b></td>
    <td class="wind_">штиль</td>
    <td class="ff_0">0</td>
    <td class="vis_2">20 км</td>
    <td class="w_sn">слаб. снег</td>
    <td class="vis_10">10/0<br>[As op Cs]</td>
    <td class="temp_30"><nobr>-21.9</nobr></td>
    <td class="temp_29"><nobr>-24.4</nobr></td>
    <td class="temp_37">80</td>
    <td class="temp_30"><nobr>-22</nobr></td>
    <td class="temp_30"><nobr>-22</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_34">1038.8</td>
    <td class="black">1021.9</td>
    <td class="temp_30"><nobr>-21.9</nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="за 12 ч." class="temp_39">0.3</td>
    <td class="temp_"></td>
    <td title="сухой снег 10 баллов" class="snow_9">36</td>
    </tr>
    <tr height="30" bgColor=#daf1f7>
    <td class=black><b>03</b></td>
    <td class=black><b>2.12</b></td>
    <td class="wind_">штиль</td>
    <td class="ff_0">0</td>
    <td class="vis_2">20 км</td>
    <td class="w_"></td>
    <td class="vis_10">10 баллов</td>
    <td class="temp_29"><nobr>-23.2</nobr></td>
    <td class="temp_28"><nobr>-25.7</nobr></td>
    <td class="temp_37">80</td>
    <td class="temp_29"><nobr>-23</nobr></td>
    <td class="temp_29"><nobr>-23</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_33">1042.8</td>
    <td class="black">1025.3</td>
    <td class="temp_29"><nobr>-23.6</nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#ffffff>
    <td class=black><b>06</b></td>
    <td class=black><b>2.12</b></td>
    <td class="wind_s">Ю</td>
    <td class="ff_1">1</td>
    <td class="vis_2">20 км</td>
    <td class="w_"> <i>{снег}</i></td>
    <td class="vis_10">10/0<br>[Ac trans Cs]</td>
    <td class="temp_30"><nobr>-21.6</nobr></td>
    <td class="temp_29"><nobr>-24.8</nobr></td>
    <td class="temp_38">75</td>
    <td class="temp_29"><nobr>-25</nobr></td>
    <td class="temp_29"><nobr>-24</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_34">1041.8</td>
    <td class="black">1024.9</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#daf1f7>
    <td class=black><b>09</b></td>
    <td class=black><b>2.12</b></td>
    <td class="wind_s">Ю</td>
    <td class="ff_2">2</td>
    <td class="vis_3">10 км</td>
    <td class="w_sn">слаб. снег</td>
    <td class="vis_10">10/0<br>[As op]</td>
    <td class="temp_30"><nobr>-20.9</nobr></td>
    <td class="temp_29"><nobr>-23.5</nobr></td>
    <td class="temp_37">80</td>
    <td class="temp_28"><nobr>-27</nobr></td>
    <td class="temp_28"><nobr>-27</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_34">1042.1</td>
    <td class="black">1025.2</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#ffffff>
    <td class=black><b>12</b></td>
    <td class=black><b>2.12</b></td>
    <td class="wind_sw">ЮЗ</td>
    <td class="ff_1">1</td>
    <td class="vis_2">20 км</td>
    <td class="w_"> <i>{снег}</i></td>
    <td class="vis_10">10/0<br>[Cs]</td>
    <td class="temp_30"><nobr>-21.4</nobr></td>
    <td class="temp_29"><nobr>-23.7</nobr></td>
    <td class="temp_37">82</td>
    <td class="temp_29"><nobr>-25</nobr></td>
    <td class="temp_29"><nobr>-25</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_33">1042.6</td>
    <td class="black">1025.7</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_30"><nobr>-20.5</nobr></td>
    <td title="за 12 ч." class="temp_39">0.2</td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#daf1f7>
    <td class=black><b>15</b></td>
    <td class=black><b>2.12</b></td>
    <td class="wind_s">Ю</td>
    <td class="ff_1">1</td>
    <td class="vis_3">10 км</td>
    <td class="w_"></td>
    <td class="vis_10">10/0<br>[Cs]</td>
    <td class="temp_30"><nobr>-20.4</nobr></td>
    <td class="temp_29"><nobr>-22.6</nobr></td>
    <td class="temp_37">82</td>
    <td class="temp_29"><nobr>-23</nobr></td>
    <td class="temp_29"><nobr>-23</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_34">1042.0</td>
    <td class="black">1025.2</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#ffffff>
    <td class=black><b>18</b></td>
    <td class=black><b>2.12</b></td>
    <td class="wind_s">Ю</td>
    <td class="ff_5">5</td>
    <td class="vis_3">10 км</td>
    <td class="w_shsn">слаб. ливневой снег</td>
    <td class="vis_10">10/10 600 м<br>[Cb cap]</td>
    <td class="temp_31"><nobr>-17.3</nobr></td>
    <td class="temp_31"><nobr>-19.4</nobr></td>
    <td class="temp_37">84</td>
    <td class="temp_28"><nobr>-27</nobr></td>
    <td class="temp_28"><nobr>-27</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_34">1039.6</td>
    <td class="black">1023.0</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#daf1f7>
    <td class=black><b>21</b></td>
    <td class=black><b>2.12</b></td>
    <td class="wind_s">Ю</td>
    <td class="ff_6">6</td>
    <td class="vis_6">4000 м</td>
    <td class="w_shsn">слаб. ливневой снег</td>
    <td class="vis_10">10/10 600 м<br>[Cb cap]</td>
    <td class="temp_32"><nobr>-16.1</nobr></td>
    <td class="temp_31"><nobr>-18.2</nobr></td>
    <td class="temp_37">84</td>
    <td class="temp_28"><nobr>-26</nobr></td>
    <td class="temp_28"><nobr>-26</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_35">1037.4</td>
    <td class="black">1020.9</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#ffffff>
    <td class=black><b>00</b></td>
    <td class=black><b>3.12</b></td>
    <td class="wind_s">Ю</td>
    <td class="ff_6">6</td>
    <td class="vis_6">4000 м</td>
    <td class="w_shsn">слаб. ливневой снег <i>{метель}</i></td>
    <td class="vis_10">10/10 600 м<br>[Cb cap]</td>
    <td class="temp_32"><nobr>-15.7</nobr></td>
    <td class="temp_31"><nobr>-17.5</nobr></td>
    <td class="temp_36">86</td>
    <td class="temp_29"><nobr>-25</nobr></td>
    <td class="temp_29"><nobr>-25</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_35">1035.2</td>
    <td class="black">1018.7</td>
    <td class="temp_29"><nobr>-22.8</nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="за 12 ч." class="temp_39">0.7</td>
    <td class="temp_"></td>
    <td title="сухой снег 10 баллов" class="snow_9">37</td>
    </tr>
    <tr height="30" bgColor=#daf1f7>
    <td class=black><b>03</b></td>
    <td class=black><b>3.12</b></td>
    <td class="wind_sw">ЮЗ</td>
    <td class="ff_5">5</td>
    <td class="vis_7">2000 м</td>
    <td class="w_shsn">ливневой снег <i>{метель}</i></td>
    <td class="vis_10">10/10 600 м<br>[Cb cap]</td>
    <td class="temp_32"><nobr>-15.4</nobr></td>
    <td class="temp_31"><nobr>-17.3</nobr></td>
    <td class="temp_37">85</td>
    <td class="temp_29"><nobr>-24</nobr></td>
    <td class="temp_29"><nobr>-24</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_35">1032.9</td>
    <td class="black">1016.5</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#ffffff>
    <td class=black><b>06</b></td>
    <td class=black><b>3.12</b></td>
    <td class="wind_sw">ЮЗ</td>
    <td class="ff_2">2</td>
    <td class="vis_7">2000 м</td>
    <td class="w_shsn">ливневой снег <i>{метель}</i></td>
    <td class="vis_10">10/10 600 м<br>[Cb cap]</td>
    <td class="temp_32"><nobr>-14.7</nobr></td>
    <td class="temp_31"><nobr>-16.6</nobr></td>
    <td class="temp_37">85</td>
    <td class="temp_30"><nobr>-20</nobr></td>
    <td class="temp_30"><nobr>-20</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_36">1032.1</td>
    <td class="black">1015.8</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#daf1f7>
    <td class=black><b>09</b></td>
    <td class=black><b>3.12</b></td>
    <td class="wind_w">З</td>
    <td class="ff_1">1</td>
    <td class="vis_6">4000 м</td>
    <td class="w_shsn">слаб. ливневой снег</td>
    <td class="vis_10">10/10 600 м<br>[Cb cap]</td>
    <td class="temp_32"><nobr>-14.7</nobr></td>
    <td class="temp_31"><nobr>-16.7</nobr></td>
    <td class="temp_37">85</td>
    <td class="temp_31"><nobr>-17</nobr></td>
    <td class="temp_31"><nobr>-17</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_35">1032.7</td>
    <td class="black">1016.4</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#ffffff>
    <td class=black><b>12</b></td>
    <td class=black><b>3.12</b></td>
    <td class="wind_n">С</td>
    <td class="ff_1">1</td>
    <td class="vis_2">20 км</td>
    <td class="w_"> <i>{ливн. осадки}</i></td>
    <td class="vis_10">10/0<br>[As trans]</td>
    <td class="temp_32"><nobr>-16.5</nobr></td>
    <td class="temp_31"><nobr>-18.5</nobr></td>
    <td class="temp_37">84</td>
    <td class="temp_31"><nobr>-19</nobr></td>
    <td class="temp_31"><nobr>-19</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_35">1035.2</td>
    <td class="black">1018.7</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_32"><nobr>-14.4</nobr></td>
    <td title="за 12 ч." class="temp_39">2</td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#daf1f7>
    <td class=black><b>15</b></td>
    <td class=black><b>3.12</b></td>
    <td class="wind_n">С</td>
    <td class="ff_1">1</td>
    <td class="vis_2">20 км</td>
    <td class="w_"></td>
    <td class="vis_10">10/0<br>[As trans]</td>
    <td class="temp_31"><nobr>-17.9</nobr></td>
    <td class="temp_30"><nobr>-19.9</nobr></td>
    <td class="temp_37">84</td>
    <td class="temp_30"><nobr>-21</nobr></td>
    <td class="temp_30"><nobr>-21</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_34">1037.8</td>
    <td class="black">1021.2</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#ffffff>
    <td class=black><b>18</b></td>
    <td class=black><b>3.12</b></td>
    <td class="wind_n">С</td>
    <td class="ff_1">1</td>
    <td class="vis_2">20 км</td>
    <td class="w_">ледяные иглы</td>
    <td class="vis_10">10 баллов</td>
    <td class="temp_30"><nobr>-20.3</nobr></td>
    <td class="temp_30"><nobr>-22.4</nobr></td>
    <td class="temp_37">83</td>
    <td class="temp_29"><nobr>-23</nobr></td>
    <td class="temp_29"><nobr>-23</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_33">1042.6</td>
    <td class="black">1025.3</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    <tr height="30" bgColor=#daf1f7>
    <td class=black><b>21</b></td>
    <td class=black><b>3.12</b></td>
    <td class="wind_n">С</td>
    <td class="ff_1">1</td>
    <td class="vis_2">20 км</td>
    <td class="w_">ледяные иглы</td>
    <td class="vis_10">10 баллов</td>
    <td class="temp_30"><nobr>-22.3</nobr></td>
    <td class="temp_29"><nobr>-24.9</nobr></td>
    <td class="temp_37">79</td>
    <td class="temp_28"><nobr>-26</nobr></td>
    <td class="temp_28"><nobr>-26</nobr></td>
    <td class="black" bgcolor=""></td>
    <td class="temp_33">1045.5</td>
    <td class="black">1028.0</td>
    <td class="temp_"><nobr></nobr></td>
    <td class="temp_"><nobr></nobr></td>
    <td title="" class="temp_"></td>
    <td class="temp_"></td>
    <td title="" class="snow_"></td>
    </tr>
    </table>
    <p>Внимание! Время в таблицах - всемирное. Для получения местного времени необходимо прибавить поправку, которая   равна 7  ч.</p>'''

# Получение html страницы с раздела сайта "Погода и климат" --> "Архив погоды". id следует взять из адресной строки браузера после перехода
# к нужному населенному пункту.
params = {'id':'29635', 'bday':'1', 'fday':'3', 'amonth':'12', 'ayear':'2018', 'bot':'2'}
'''r = requests.get('http://www.pogodaiklimat.ru/weather.php', params)
r.encoding = 'utf-8'
t = r.text
'''
# Взятие поправки к UTC из html страницы.
stringUTC = t[t.find('<p>Внимание!'):t.find('ч.</p>')]
stringUTC = stringUTC.rstrip()
regexes = [re.compile(str(i)) for i in range(13)]
for regex in regexes:
    if regex.search(stringUTC):
        deltaTime = int(regex.pattern)

# Выпиливаем нужное из таблицы html файла. То, что нужно, по порядку перечислено в listOfParams.
tableInString = t[t.find('</tr'):t.find('</table')]
tableInString = tableInString.strip('</tr>').strip('\n').split('</tr>')
del tableInString[-1]
tableInString = [i.split('<td') for i in tableInString] # ...еще нарезка строк.

    # Выбираем строки с нужной информацией, удаляем мешающие извлечению данных тэги.
tableInString = [[i[1].replace('<b>', ''), i[2].replace('<b>', ''), i[3], i[4],
                  i[8].replace('<nobr>', ''), i[10], i[15], i[16].replace('<nobr>', ''),
                  i[17].replace('<nobr>', ''), i[18], i[20]] for i in tableInString]

    # Выборка данных и заполнение итогового списка.
listOfData = []
n = 0
for i in tableInString:
    listOfData.append([])
    for j in i:
        data = j[j.find('>') + 1:j.find('<')]
        listOfData[n].append(data)
        if i.index(j) == 10:                        # Получение данных по виду снежного покрова из последней строки.
            data = j[j.find('"') + 1:j.find('" ')]
            listOfData[n].append(data)
    n += 1

# Поправка на местное время c коррекцией даты. Первод давления из ГПа в мм рт. ст.
for i in listOfData:
    data = i[1].split('.')
    timeEpoch = time.mktime((int(params['ayear']), int(data[1]), int(data[0]), int(i[0]) + deltaTime, 0, 0, 0, 0, 0))
    parsedTime = time.strptime(time.ctime(timeEpoch))
    i[0] = str(parsedTime.tm_hour)
    i[1] = str(parsedTime.tm_mday) + '.' + str(parsedTime.tm_mon) + '.' + str(parsedTime.tm_year)
    i[6] = '%.1f' % (float(i[6]) * 0.750063755419211)

print(listOfData)