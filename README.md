# pengolahan-citra_uts

**Nama : Muhamad Valentino Ramzi

Kelas : I241E

Matkul : Pengolahan Citra 

Dosen Pengampu : Dr. Muhamad Fatchan, S.Kom.,M.Kom.

# 📌 Praktikum 8 — Segmentasi Citra Digital

**Topik:** Segmentasi Citra Menggunakan Python & OpenCV

---

## 📷 1. Pembuatan Citra Sintetis

Citra sintetis dibuat sebagai data uji untuk seluruh proses segmentasi.

Proses yang dilakukan:

* Membuat background abu-abu
* Menambahkan noise (bintik acak)
* Menggambar beberapa objek berbentuk lingkaran
* Memberikan efek blur agar citra lebih halus

👉 Citra ini digunakan sebagai input utama di semua metode.

---

## 🎯 2. Thresholding

![Threshold](https://github.com/ramzi121006/pengolahan-citra_uts/blob/5ddfc4de0edc63d97f04f588fad43e63fddce1af/ss_citra/hasil%20thresholding.png)

Pada tahap ini dilakukan segmentasi menggunakan tiga metode:

* **Global Threshold** → menggunakan nilai tetap (128)
* **Otsu** → otomatis mencari threshold terbaik
* **Adaptif** → threshold berbeda di setiap area

### 🧠 Analisis:

* Global kurang fleksibel
* Otsu lebih optimal
* Adaptif paling stabil untuk variasi cahaya

---

## 🌱 3. Region Growing

![Region](https://github.com/ramzi121006/pengolahan-citra_uts/blob/f4c253c1447f1889fabaf912173f7b29c7ac01ad/ss_citra/region.png)

Metode ini mengambil area berdasarkan titik awal (*seed*).

### 🧠 Analisis:

* Threshold kecil → area sempit
* Threshold besar → area luas
* Posisi seed sangat mempengaruhi hasil

👉 Cocok untuk segmentasi berbasis area tertentu

---

## 🧩 4. Deteksi Tepi

![Edge](output/edge.png)

Digunakan untuk mendeteksi batas objek:

* **Sobel** → mendeteksi arah gradien
* **Canny** → hasil paling jelas dan rapi

### 🧠 Analisis:

Canny memberikan hasil terbaik karena noise lebih terkontrol.

---

## 🎨 5. K-Means Clustering

![KMeans](output/kmeans.png)

Mengelompokkan pixel berdasarkan kemiripan intensitas.

### 🧠 Analisis:

* K kecil → hasil kasar
* K besar → lebih detail
* Pemilihan K sangat penting

---

## 🌊 6. Watershed

![Watershed](output/watershed.png)

Digunakan untuk memisahkan objek yang saling menempel.

Proses:

* Thresholding
* Distance Transform
* Penandaan marker
* Segmentasi

### 🧠 Analisis:

* Objek yang menempel berhasil dipisahkan
* Boundary terlihat jelas

---

## 📊 7. Evaluasi (IoU & Dice)

![Evaluasi](output/evaluasi.png)

Evaluasi dilakukan dengan membandingkan hasil segmentasi dengan ground truth.

### 🧠 Penjelasan:

* **IoU (Intersection over Union)**
  Mengukur overlap antara hasil dan ground truth

* **Dice Similarity**
  Mengukur tingkat kesamaan dua area

### 📈 Interpretasi:

* Nilai mendekati 1 → hasil sangat baik
* Nilai kecil → segmentasi kurang akurat

---

## 🚀 Kesimpulan

Metode segmentasi memiliki kelebihan masing-masing:

* Thresholding → cepat & sederhana
* Region Growing → berbasis area
* Edge Detection → fokus pada batas
* K-Means → berbasis clustering
* Watershed → terbaik untuk objek menempel

👉 Kombinasi metode memberikan hasil yang lebih optimal.

---

## 🛠️ Tools

* Python
* OpenCV
* NumPy
* Matplotlib

---
