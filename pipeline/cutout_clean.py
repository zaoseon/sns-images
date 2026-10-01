"""밝은 배경용 누끼 정리(10/1 시험 결과 채택). 원본 누끼는 가장자리에 회색 외곽선·머리카락 잔상이 남아 흰/크림 바탕에서 지저분하다.
방법: 가장자리·반투명 픽셀의 색을 가장 가까운 '확실한 안쪽' 픽셀 색으로 바꾸고(색 번짐 제거), 알파를 1px 줄인 뒤 살짝 풀어 준다.
사용: python3 pipeline/cutout_clean.py  -> characters/cut_light/*.png"""
import os, glob, numpy as np
from PIL import Image, ImageFilter
import scipy.ndimage as ndi
HERE = os.path.dirname(os.path.abspath(__file__))
def clean(im, erode=1, feather=1.0, solid_thr=0.97):
    a = np.array(im.convert("RGBA")).astype(np.float32); alpha = a[..., 3] / 255.
    solid = alpha > solid_thr
    idx = ndi.distance_transform_edt(~solid, return_distances=False, return_indices=True)
    rgb = a[..., :3][idx[0], idx[1]]
    al = Image.fromarray((alpha * 255).astype(np.uint8))
    for _ in range(erode): al = al.filter(ImageFilter.MinFilter(3))
    al = al.filter(ImageFilter.GaussianBlur(feather))
    return Image.fromarray(np.dstack([rgb, np.array(al, dtype=np.float32)]).astype(np.uint8), "RGBA")
if __name__ == "__main__":
    src = os.path.join(HERE, "..", "characters", "cut"); dst = os.path.join(HERE, "..", "characters", "cut_light"); os.makedirs(dst, exist_ok=True)
    for p in sorted(glob.glob(src + "/v*.png")): clean(Image.open(p)).save(os.path.join(dst, os.path.basename(p)))
