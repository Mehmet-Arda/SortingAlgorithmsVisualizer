# Sıralama Algoritmaları Görselleştiricisi

## Açıklama

Bu proje, kullanıcıdan alınan listeye, 4 farklı sıralama algoritmasının (Selection-Bubble-Insertion-Merge-Quick) uygulanışını, 3 farklı grafik türüyle (Scatter-Bar-Stem) animasyon şeklinde görselleştirilmesini sağlayan bir masaüstü uygulamasıdır.

Kullanıcıdan başlangıçta, manuel ya da rastgele olacak şekilde bir liste alınmaktadır. Girilen liste, seçilen algoritmaya göre sıralanmakta ve seçilen grafik türüne göre animasyon başlatılmaktadır.

Proje, temelinde Python programlama diliyle yazılmıştır. Masaüstü uygulaması için PyQt5 kütüphanesi kullanılırken, görselleştirme ve animasyon işlemleri için ise Matplotlib kütüphanesi kullanılmıştır.


## Çekirdek Teknolojiler

- [Python](https://www.python.org/)

- [Qt](https://www.qt.io/)

- [PyPI](https://pypi.org)

## Gerekli Kütüphaneler

- [PyQt5](https://pypi.org/project/PyQt5/)

- [Matplotlib](https://matplotlib.org/)

- [Numpy](https://numpy.org/)

- [PyInstaller](https://pypi.org/project/pyinstaller/)

- [Google Fonts](https://fonts.google.com/)


## Geliştirme

- [Visual Studio Code](https://code.visualstudio.com/)


## İndirme

Proje, "pyinstaller" modülü ile tek bir .exe uzantılı uygulama haline getirilmiştir. Bu uygulama, kaynak dosyalar içerisinden "/dist" klasörü altında bulunmaktadır.
Başka herhangi bir dosyaya gerek kalmaksızın sadece bu uygulama ile proje çalıştırılabilmektedir.



## Uygulama Özellikleri/Kullanımı

1. **Uygulama Arayüzü**

![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/a7c033a6-d4b4-428e-89e4-0360fffc0d24)


2. **Manuel/Rastgele Liste Girme**

   - Uygulamada ilk olarak manuel ya da rastgele şekilde bir liste girilmektedir.

   ![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/16cf8da8-e822-477b-b65e-133edaed3b0f)


   - **Manuel liste ile:**
      
     ![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/9cff208d-9528-4106-81ed-869ebdb5955e)

     - Listeye eleman ekledikçe sağa doğru scrollbar ilerlemektedir.

     ![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/ff88e47e-09d6-413c-9d2f-2b45f0e9b356)
     
     ![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/ed840e26-e085-4ffd-b63c-170827160e47)


     - Liste elemanları, "Çıkar" butonu ile tek tek silinebilmektedir.

     ![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/421b3560-f055-4c8f-95bb-953a4c002a8e)

     - Liste elemanları, "Temizle" butonu ile tamamen silinebilmektedir.

     ![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/fd6c9fca-7128-4a82-af7a-0c871f53c6c1)


    - **Rastgele Liste ile:**
    
      - Rastgele liste için kullanıcı, listenin alabileceği minimum ve maksimum değerleri ile birlikte listenin eleman adedini girebilmektedir.

      ![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/29a336bd-42fd-4702-878c-d3d801bdceae)
    
      ![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/b95b8c98-9e8a-4896-ab25-e83635315e0a)
      
            

3. **Kontrol Butonları**

   - Kullanıcı geçerli bir liste girdiğinde arayüzde bulunan kontrol butonlarından "Oluştur" butonu aktifleşmektedir.

    ![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/8e0edfcb-d249-4b9a-a7a1-524c1b93c0a0)
    
    ![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/009a02a9-37fe-4771-869e-28f3b0474627)



4. **Sıralama Algoritması ve Grafik Türü Seçimi**

    - Kullanıcı, arayüz üzerindeki radio butonları ile listeye uygulanması istediği sıralama algoritması ve grafik türünü seçebilmektedir. Herhangi bir seçim yapılmadıkça varsayılan değerler "Kabarcık Sıralaması-Sütun Grafiği"dir.
  
    ![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/b458a1ba-de01-4c05-80eb-c49f81fdf1bb)

    - "Oluştur" butonuna basıldığında, istenilen parametrelere göre grafik çizilmektedir.
  
    ![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/c4d4d564-0c46-4e65-bb1c-f7a93a96a266)






5. **Animasyon Hızı**

    - Grafik animasyonunun hızı, arayüz üzerindeki slider üzerinden değiştirilebilmektedir.

    ![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/80b75bc7-55bb-4c44-8537-6f4fc973abd6)


6. **Animasyonun Başlatılması**

    - "Başlat" butonuna tıklanıldığında animasyon başlatılmaktadır.

    ![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/c1cad11e-5853-4e9c-9a6c-dc9dda1dc6ac)



7. **Durdurma/Devam Etme**

    - "Durdur-Devam Et" butonlarına tıklandığında, animasyon durdurulup, kaldığı yerden devam ettirilebilmektedir.

  


8. **Sıfırlama**

    - Animasyon bittiğinde ya da animasyonun herhangi bir anında, tüm animasyon ve grafik sıfırlanabilmektedir.

    ![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/8b3c63cf-04d0-41ab-afa1-c4e63afe777b)
    
     
    ![image](https://github.com/Mehmet-Arda/SortingAlgorithmsVisualizer/assets/56768017/03687fd6-bc31-467b-ba99-16b14cc30ddd)





