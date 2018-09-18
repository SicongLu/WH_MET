'''
This intends to reocrd some favorable color scheme, recorded based on color hex code.
It could be used by ROOT.GetColor(color_str)
'''
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def get_berkeley_palette():
    '''http://brand.berkeley.edu/colors/#palettes'''
    palette = {}
    #Core
    palette["Berkeley Blue"] = "003262"
    palette["Founders Rock"] = "3B7EA1"
    palette["California Gold"] = "FDB515"
    palette["Medalist"] = "C4820E"
    
    #Accent
    palette["Wellman Tile"] = "D9661F"
    palette["Rose Garden"] = "EE1F60"
    palette["Golden Gate"] = "ED4E33"
    palette["South Hall"] = "6C3302"
    palette["Bay Fog"] = "DDD5C7"
    palette["Lawrence"] = "00B0DA"
    palette["Lap Lane"] = "00A598"
    palette["Pacific"] = "46535E"
    palette["Sather Gate"] = "B9D3B6"
    palette["Ion"] = "CFDD45"
    palette["Soybean"] = "859438"
    palette["Stone Pine"] = "584F29"
    
    #Neutral
    palette["Grey"] = "EEEEEE"
    palette["Web Grey"] = "888888"
    
    palette["default_hist"] = ["California Gold","Berkeley Blue",\
    "Rose Garden","Pacific","Soybean","Web Grey","Medalist",
    ]
    #Intermediate
    palette["Green"] = "56BDA2"
    palette["colz_name_list"] = ["Berkeley Blue", "Founders Rock", "Green", "California Gold"]
    palette["rgb_list"] = [hex_to_rgb(palette[name]) for name in palette["colz_name_list"]]
    palette["stop_list"] = [0.0, 0.33, 0.67, 1.0]
    palette["line_color"] = "C4820E"
    
    return palette
    
def get_ucsd_palette():
    '''https://ucpa.ucsd.edu/brand/elements/color-palette/'''
    palette = {}
    #Core
    palette["Pantone 2767"] = "182B49"
    palette["Pantone 3015"] = "006A96"
    palette["Pantone 1245"] = "C69214"
    palette["Pantone 116"] = "FFCD00"
    
    #Accent
    palette["Pantone 3115"] = "00C6D7"
    palette["Pantone 7490"] = "6E963B"
    palette["Pantone 3945"] = "F3E500"
    palette["Pantone 144"] = "FC8900"
    
    #Neutral
    palette["Black"] = "000000"
    palette["Pantone Cool Gray 9"] = "747678"
    palette["Pantone 401"] = "B6B1A9"
    palette["Pantone 871"] = "84754e"
    
    #Self Defined
    palette["Intermediate"] = "F3E564" 
    
    palette["default_hist"] = ["Pantone 116", "Pantone 3015",\
    "Pantone 144","Pantone 7490","Pantone Cool Gray 9",\
    "Pantone 871","Pantone 2767",
    ]
    palette["colz_name_list"] = ["Pantone 3015", "Pantone 3115", "Intermediate", "Pantone 116", "Pantone 144"]
    palette["rgb_list"] = [hex_to_rgb(palette[name]) for name in palette["colz_name_list"]]
    palette["stop_list"] = [0, 0.25, 0.5, 0.75, 1.0]
    #Colz guide:
    #Blue as base, gold/medalist as texts/lines
    palette["colz_base_rgb"] = [0,106,150]
    palette["colz_high_rgb"] = [255,205,0]
    palette["line_color"] = "000000"
    return palette
def get_upenn_palette():
    '''https://www.upenn.edu/about/styleguide-color-type'''
    #Core
    palette["Shield Blue"] = "01256E"
    palette["Shield Red"] = "95001A"
    
    #Accent
    palette["Yellow"] = "F2C100"
    palette["Green"] = "008E00"
    palette["Orange"]= "C35A00"
    palette["Purple"] = "4A0042"
    
    #Neutral
    palette["Dark Gray"] = "44464B"
    palette["Medium Gray"] = "6C6F76"
    palette["Light Gray"] = "CFD0D2"
    palette["Dark Orange"] = "AC3C00"
    palette["Lightest Orange"] = "EFCB80"
    
    #Intermediate
    palette["Lighter Blue"] = "045EA7"
    palette["colz_name_list"] = ["Shield Blue", "Lighter Blue", "Yellow", "Orange", "Shield Red"]
    palette["rgb_list"] = [hex_to_rgb(palette[name]) for name in palette["colz_name_list"]]
    palette["stop_list"] = [0.0, 0.4, 0.6, 0.8, 1.0]
    
    palette["default_hist"] = ["Shield Red", "Shield Blue",\
    "Yellow","Green","Orange","Purple","Dark Gray",
    ]
    #palette["colz_base_rgb"] = [1,37,110]
    #palette["colz_high_rgb"] = [149,0,26]
    palette["line_color"] = "95001A" 
    
    #Colz guide:
    #Blue as base, gold/medalist as texts/lines
    return palette
import ROOT
import array
def get_colz_palette_old(rgb_list):
    '''This will return a color table for SetPalette for Colz.'''
    scale = 225./max(base_rgb)
    base_rgb = [1.0*col/255. for col in base_rgb]
    if high_rgb != False:
        high_rgb = [1.0*col/255. for col in high_rgb]
        number = 3
        stops = array.array('d',[0, 0.5, 1.0])
        red   = array.array('d',[base_rgb[0], base_rgb[0]*scale, high_rgb[0]])
        green = array.array('d',[base_rgb[1], base_rgb[1]*scale, high_rgb[1]])
        blue  = array.array('d',[base_rgb[2], base_rgb[2]*scale, high_rgb[2]])
    else:
        number = 3
        stops = array.array('d',[0, 0.5, 1.0])
        red   = array.array('d',[base_rgb[0]/2., base_rgb[0], base_rgb[0]*scale])
        green = array.array('d',[base_rgb[1]/2., base_rgb[1], base_rgb[1]*scale])
        blue  = array.array('d',[base_rgb[2]/2., base_rgb[2], base_rgb[2]*scale])
    FI = ROOT.TColor.CreateGradientColorTable(number,stops, red, green, blue, ncolors)
    color_table = [FI+i for i in range(ncolors)]
    color_table = array.array('i',color_table)		
    
    return  color_table
def get_colz_palette(rgb_list, stop_list, ncolors):
    '''This will return a color table for SetPalette for Colz.'''
    r_list = [item[0]/255. for item in rgb_list]
    g_list = [item[1]/255. for item in rgb_list]
    b_list = [item[2]/255. for item in rgb_list]
    number = len(r_list)
    red = array.array('d',r_list)
    green = array.array('d',g_list)
    blue = array.array('d',b_list)
    stops = array.array('d',stop_list)

    FI = ROOT.TColor.CreateGradientColorTable(number, stops, red, green, blue, ncolors)
    color_table = [FI+i for i in range(ncolors)]
    color_table = array.array('i',color_table)		
    
    return  color_table

def draw_example(color_table, line_col):
    c3 = ROOT.TCanvas("canvas","canvas",0,0,800,400);
    c3.Divide(2,1);
    f3 = ROOT.TF2("f3","0.1+(1-(x-2)*(x-2))*(1-(y-2)*(y-2))",1,3,1,3);
    f3.SetLineWidth(1);
    print(line_col)
    f3.SetLineColor(ROOT.TColor.GetColor(line_col)); 
    f3.SetLineWidth(2);
    c3.cd(1);
    f3.Draw("surf2");
    ROOT.gStyle.SetPalette(len(color_table),color_table)
    c3.cd(2);
    f3.Draw("colz");
    
    c3.Update()
    c3.Draw()
    c3.Print("test_palette.png")
    return c3;

if __name__=="__main__":
    palette = get_berkeley_palette()
    #palette = get_ucsd_palette()
    #palette = get_upenn_palette()
    col_table = get_colz_palette(palette["rgb_list"],palette["stop_list"], ncolors = 100)
    #col_table2 = get_colz_palette(palette["colz_base_rgb"], False, ncolors = 100)
    draw_example(col_table, "#"+palette["line_color"])
    
    