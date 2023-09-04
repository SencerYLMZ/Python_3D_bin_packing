from py3dbp import Packer, Bin, Item
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

packer = Packer()

# Konteyner boyutlarını al
genislik_kont = float(input("Konteyner genişliğini giriniz: "))
yukseklik_kont = float(input("Konteyner yüksekliğini giriniz: ")) 
derinlik_kont = float(input("Konteyner derinliğini giriniz: ")) 
max_weight = float(input("Konteynerin taşıyabileceği maksimum ağırlığı giriniz: "))
konteyner_boyutları = [genislik_kont, yukseklik_kont, derinlik_kont]
kont_hacim = float(genislik_kont * yukseklik_kont * derinlik_kont)

#Konteyner oluştur.
kont = Bin("Konteyner", genislik_kont, yukseklik_kont, derinlik_kont, max_weight)
packer.add_bin(kont)

# İçine yerleştirilecek silindirik cisim
toplam_ağırlık = 0
toplam_hacim = 0
un_fitted= []
a = input("Silindirik bir cisim yerleştirmek istiyor musunuz ?  E/H \n")

if a.lower() == "e":
    
    tür_silindir = int(input("Kaç tür silindirik cisim girilecek: "))
    
    for i in range(1, tür_silindir + 1):
        
        R = float(input(f"{i}. tür Silindirik cismin yarıçapını giriniz: "))
        H = float(input(f"{i}. tür Silindirik cismin uzunluğunu giriniz: "))
        silindir_ağırlık = float(input(f"{i}. tür silindirik cismin ağırlığını giriniz: "))
        tane_silindir = int(input(f"{i}. tür silindirik cisimden kaç tane istediğinizi yazınız: "))
        silindir_hacim = 2*R * H * 2*R
        
        for tane in range(1, tane_silindir + 1):
            
            if silindir_ağırlık <= max_weight and silindir_hacim <= kont_hacim:
                toplam_ağırlık += silindir_ağırlık
                toplam_hacim += silindir_hacim
            
            if silindir_ağırlık > max_weight or silindir_hacim > kont_hacim:
                
                print("Silindirik nesne konteynerin hacim ve/veya ağırlık kapasitesini aşıyor. Eklenmedi.")
                un_fitted.append(f"{i} tür {tane}. silindirik cisim")
                
                break 
            
            if toplam_ağırlık < max_weight and toplam_hacim < kont_hacim:
                
                    b = Item("Silindirik cisim", 2*R, H, 2*R, silindir_ağırlık)  
                    packer.add_item(b) 
                    
            elif toplam_ağırlık == max_weight or toplam_hacim == kont_hacim:
                    print("Toplam ağırlık maksimum taşıma kapasitesine ulaşmış durumda.")
                    
                    b = Item("Silindirik cisim", 2*R, H, 2*R, silindir_ağırlık)  
                    packer.add_item(b)  
            else: 
                
                print("Silindirik nesne konteynerin boyut veya ağırlık kapasitesini aşıyor. Eklenmedi.")
                un_fitted.append(f"{i} tür {tane}. silindirik cisim")
        

    
# İçine yerleştirilecek paletler   

A = int(input("Lütfen konteyner'ın içine kaç tür palet koyulacağını yazınız:"))

for i in range(1, A + 1):
       
    genişlik = float(input(f"{i}. tür cismin genişliğini giriniz: ")) 
    yükseklik = float(input(f"{i}. tür cismin yüksekliğini giriniz: ")) 
    derinlik = float(input(f"{i}. tür cismin derinliğini giriniz: ")) 
    ağırlık = float(input(f"{i}. tür cismin ağırlığını giriniz: ")) 
    tane = int(input("Bu ölçüdeki nesneden kaç tane istediğinizi yazın: "))
    cisim_hacim = float(genişlik * yükseklik * derinlik)
    for a in range(1, tane + 1):    
    
        if ağırlık <= max_weight and cisim_hacim <= kont_hacim:   
        
            toplam_ağırlık += ağırlık
            toplam_hacim += cisim_hacim
        
        if ağırlık > max_weight or cisim_hacim > kont_hacim:
            
            print(f"{i}. tür nesne konteynerin boyut veya ağırlık kapasitesini aşıyor. Eklenmedi.")
            un_fitted.append(f"{i}. tür {a}. nesne")
            
            break
        
        if toplam_ağırlık < max_weight and toplam_hacim < kont_hacim:
                   
            
            b = Item(f"{i}. tür {a}. cisim", genişlik, yükseklik, derinlik, ağırlık)
            packer.add_item(b)
            
        elif toplam_ağırlık == max_weight or toplam_hacim == kont_hacim: 
            
            b = Item(f"{i}. cisim", genişlik, yükseklik, derinlik, ağırlık)
            packer.add_item(b)
        
            print("Toplam ağırlık maksimum taşıma kapasitesine ulaşmış durumda.")
            break
        else:
            print(f"{i}. tür nesne konteynerin boyut ve/veya ağırlık kapasitesini aşıyor. Eklenmedi.")
            un_fitted.append(f"{i}. tür {a}. nesne")
        
# Nesneleri yerleştirme işlemini gerçekleştir

packer.pack(bigger_first=True, distribute_items=False, number_of_decimals=3)

# Yerleştirilemeyen nesneler
print("\nYerleştirilemeyen nesneler:")

for i in packer.bins:
    
    if len(i.unfitted_items) == 0 and len(un_fitted) == 0:
        
        print("Yerleştirilemeyen nesne yok.")
    else:   
        
        for unfitted in i.unfitted_items:
            
            print(unfitted.string())
       
        print(un_fitted)    
#3D çizim

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection = "3d")
ax.set_xlim(0, 15)  # x düzlemi sınırları
ax.set_ylim(0, 15)  # y düzlemi sınırları
ax.set_zlim(0, 15)  # z düzlemi sınırları


# konteyner'ın çizimi
vertices = [
    [0, 0, 0],
    [konteyner_boyutları[0], 0, 0],
    [konteyner_boyutları[0], konteyner_boyutları[2], 0],  
    [0, konteyner_boyutları[2], 0],  
    [0, 0, konteyner_boyutları[1]],  
    [konteyner_boyutları[0], 0, konteyner_boyutları[1]],  
    [konteyner_boyutları[0], konteyner_boyutları[2], konteyner_boyutları[1]],  
    [0, konteyner_boyutları[2], konteyner_boyutları[1]]  
]

faces = [
    [vertices[0], vertices[1], vertices[2], vertices[3]], # Alt yüzey
    [vertices[4], vertices[5], vertices[6], vertices[7]], # Üst yüzey
    [vertices[0], vertices[1], vertices[5], vertices[4]], # Cephe 1
    [vertices[1], vertices[2], vertices[6], vertices[5]], # Cephe 2 
    [vertices[2], vertices[3], vertices[7], vertices[6]], # Cephe 3
    [vertices[3], vertices[0], vertices[4], vertices[7]]  # Cephe 4
]

ax.add_collection3d(Poly3DCollection(faces, facecolors='white', edgecolors='black', alpha=0.0))


# Yerleştirilen her bir nesneyi grafiğe ekleyin
beyaz_kutular = []
for item in packer.bins:
    
    for fitted in item.items:
        
        x, y, z = fitted.position  # X, Y, Z pozisyonu
            
        width, height, depth = fitted.get_dimension()  # X, Y, Z boyutu
        
        if fitted.name == "Silindirik cisim":
    
            beyaz_kutu= ax.bar3d(x, z, y, width, depth, height, shade=True, color = "white", edgecolors = "white", alpha = 0.0 )
            beyaz_kutular.append(beyaz_kutu)
                      
        else: 
             
            ax.bar3d(x, z, y, width, depth, height, shade=True, edgecolors = "red")


for i, beyaz_kutu in enumerate(beyaz_kutular):
    
    fitted = packer.bins[0].items[i] 
    
    d, e, f = fitted.position # x, y, z = d, e, f karışıklık olmaması adına d, e, f 
    genislik, yukseklik, derin = fitted.get_dimension()
    
    
    theta = np.linspace(0, 2*np.pi, 100)
    z_degerleri = np.linspace(0, H, 100)
    theta, z_degerleri = np.meshgrid(theta, z_degerleri)

    if genislik > yukseklik and genislik > derin:
        # sağa ya da sola doğru yatık silindir
        x_degerleri = (R * np.cos(theta)) + float(f) + R
        y_degerleri = z_degerleri + float(d) 
        z_degerleri = (R * np.sin(theta)) + float(e) + R 
        ax.plot_surface(y_degerleri , x_degerleri , z_degerleri , alpha=1)
    
    elif genislik == yukseklik and genislik < derin:
        # öne ya da arkaya doğru yatık silindir
        x_degerleri = (R * np.cos(theta)) + float(d) + R
        y_degerleri = z_degerleri + float(f) 
        z_degerleri = (R * np.sin(theta)) + float(e) + R 
        ax.plot_surface(x_degerleri , y_degerleri , z_degerleri , alpha=1)
         
    else: 
        x_degerleri = (R * np.cos(theta)) + R + float(d)
        y_degerleri = (R * np.sin(theta)) + R + float(f)
        z_degerleri = z_degerleri + float(e)
        ax.plot_surface(x_degerleri , y_degerleri , z_degerleri , alpha=1)
  
            
ax.set_xlabel('Genişlik')
ax.set_ylabel('Derinlik')
ax.set_zlabel('Yükseklik')
ax.set_title('Paketleme Optimizasyonu Görselleştirmesi')
   
plt.show()    
