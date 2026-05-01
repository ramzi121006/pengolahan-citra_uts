# ============================================================ 
# PENGOLAHAN CITRA DIGITAL — SEGMENTASI CITRA 
# ============================================================ 

import cv2 
import numpy as np 
import matplotlib
matplotlib.use('TkAgg')  
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches 
from collections import deque 
from skimage.segmentation import watershed 
from skimage.feature import peak_local_max 
from skimage.measure import label 
from scipy import ndimage 
import os

# =========================
# UTILITAS
# =========================
def buat_citra_sintetis(ukuran=256): 
    print("Membuat citra sintetis...")
    img = np.full((ukuran, ukuran), 50, dtype=np.uint8) 
    noise = np.random.randint(0, 20, (ukuran, ukuran), dtype=np.uint8) 
    img = cv2.add(img, noise) 

    objek = [ 
        (80,80,45,200),(180,80,35,160),(80,180,30,220),
        (190,175,40,180),(128,128,20,240)
    ] 

    for (cx,cy,r,val) in objek: 
        cv2.circle(img,(cx,cy),r,val,-1) 

    img = cv2.GaussianBlur(img,(3,3),0) 
    return img 


def tampilkan_hasil(judul_besar, gambar_list, judul_list, cmap_list=None, simpan=None):
    print(f"Menampilkan: {judul_besar}")

    n = len(gambar_list)
    cols = min(n,4)
    rows = (n+cols-1)//cols

    fig, axes = plt.subplots(rows, cols, figsize=(cols*4, rows*3.5))
    fig.suptitle(judul_besar, fontsize=14, fontweight='bold')

    axes = np.array(axes).flatten() if n>1 else [axes]

    for i, ax in enumerate(axes):
        if i < n:
            cmap = (cmap_list[i] if cmap_list else None) or 'gray'
            ax.imshow(gambar_list[i], cmap=cmap)
            ax.set_title(judul_list[i])
        ax.axis('off')

    plt.tight_layout()

    if simpan:
        os.makedirs("output", exist_ok=True)
        path = "output/" + simpan
        plt.savefig(path)
        print(f"Gambar disimpan ke: {path}")

    plt.show()


# =========================
# THRESHOLDING
# =========================
def demo_thresholding(img):
    print("Proses Thresholding...")

    _, global_t = cv2.threshold(img,128,255,cv2.THRESH_BINARY)
    _, otsu = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    adaptif = cv2.adaptiveThreshold(
        img,255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,31,5
    )

    tampilkan_hasil(
        "Thresholding",
        [img, global_t, otsu, adaptif],
        ["Asli","Global","Otsu","Adaptif"],
        simpan="threshold.png"
    )


# =========================
# REGION GROWING
# =========================
def demo_region_growing(img):
    print("Proses Region Growing...")

    def region_growing(citra, seed, threshold=30):
        h, w = citra.shape
        visited = np.zeros((h,w), dtype=bool)
        mask = np.zeros((h,w), dtype=bool)

        queue = [seed]
        visited[seed] = True
        seed_val = int(citra[seed])

        while queue:
            y,x = queue.pop(0)
            mask[y,x] = True

            for dy in [-1,0,1]:
                for dx in [-1,0,1]:
                    ny, nx = y+dy, x+dx

                    if 0<=ny<h and 0<=nx<w and not visited[ny,nx]:
                        visited[ny,nx] = True
                        if abs(int(citra[ny,nx]) - seed_val) <= threshold:
                            queue.append((ny,nx))

        return mask

    seed = (80,80)
    mask = region_growing(img, seed)

    overlay = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    overlay[mask] = [0,255,0]

    tampilkan_hasil(
        "Region Growing",
        [img, overlay],
        ["Asli","Region"],
        simpan="region.png"
    )


# =========================
# EDGE DETECTION
# =========================
def demo_edge(img):
    print("Proses Edge Detection...")

    sobelx = cv2.Sobel(img,cv2.CV_64F,1,0)
    sobely = cv2.Sobel(img,cv2.CV_64F,0,1)

    sobel = cv2.magnitude(sobelx,sobely)
    sobel = np.uint8(np.clip(sobel,0,255))

    canny = cv2.Canny(img,50,150)

    tampilkan_hasil(
        "Edge Detection",
        [img, sobel, canny],
        ["Asli","Sobel","Canny"],
        simpan="edge.png"
    )


# =========================
# KMEANS
# =========================
def demo_kmeans(img):
    print("Proses KMeans...")

    Z = img.reshape((-1,1)).astype(np.float32)

    criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,100,0.2)
    K = 3
    _,label,center = cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]
    res = res.reshape(img.shape)

    tampilkan_hasil(
        "KMeans",
        [img,res],
        ["Asli","KMeans"],
        simpan="kmeans.png"
    )


# =========================
# WATERSHED
# =========================
def demo_watershed(img):
    print("Proses Watershed...")

    _, thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2,5)

    _, sure_fg = cv2.threshold(dist_transform, 0.5*dist_transform.max(),255,0)
    sure_fg = np.uint8(sure_fg)

    unknown = cv2.subtract(sure_bg, sure_fg)

    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown==255] = 0

    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    markers = cv2.watershed(img_color, markers)

    img_color[markers == -1] = [255,0,0]

    tampilkan_hasil(
        "Watershed",
        [img, thresh, dist_transform, img_color],
        ["Asli","Threshold","Distance","Hasil"],
        cmap_list=['gray','gray','hot',None],
        simpan="watershed.png"
    )
    # =========================
# EVALUASI SEGMENTASI
# =========================
def hitung_iou(mask1, mask2):
    intersection = np.logical_and(mask1, mask2).sum()
    union = np.logical_or(mask1, mask2).sum()
    return intersection / union if union != 0 else 0


def hitung_dice(mask1, mask2):
    intersection = np.logical_and(mask1, mask2).sum()
    return (2 * intersection) / (mask1.sum() + mask2.sum()) if (mask1.sum()+mask2.sum()) != 0 else 0


def demo_evaluasi(img):
    print("Proses Evaluasi...")

    # Ground truth sederhana (threshold tinggi dianggap objek)
    _, gt = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY)

    # Prediksi (pakai Otsu)
    _, pred = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    gt_bool = gt.astype(bool)
    pred_bool = pred.astype(bool)

    iou = hitung_iou(gt_bool, pred_bool)
    dice = hitung_dice(gt_bool, pred_bool)

    print(f"IoU  : {iou:.4f}")
    print(f"Dice : {dice:.4f}")

    tampilkan_hasil(
        "Evaluasi Segmentasi",
        [img, gt, pred],
        ["Asli", "Ground Truth", "Prediksi"],
        simpan="evaluasi.png"
    )


# =========================
# MAIN
# =========================
def main():
    print("Program mulai...\n")

    img = buat_citra_sintetis()

    demo_thresholding(img)
    demo_region_growing(img)
    demo_edge(img)
    demo_kmeans(img)
    demo_watershed(img)  # 🔥 tambahan terakhir
    demo_evaluasi(img)   # 🔥 terakhir

    print("\nSelesai semua proses!")


if __name__ == "__main__":
    main()