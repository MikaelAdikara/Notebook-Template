# Debugging Tanpa AI — Panduan Cepat

## 1. Cara membaca error (traceback)
1. Lihat **baris paling bawah**: `JenisError: pesan`. Ini inti masalahnya.
2. Naik ke atas, cari baris **kode milikmu** (bukan file di `site-packages`) yang paling bawah → di situ error dipicu.
3. Cek variabel yang terlibat: `print(type(x), getattr(x, "shape", None))`, `df.dtypes`, `df.columns.tolist()`.
4. Perkecil masalah: jalankan baris yang error di cell baru dengan data kecil (`df.head(100)`).
5. Cari pesan error persis (tanpa nama variabelmu) di Stack Overflow / dokumentasi.

## 2. Tabel error umum → solusi

| Error | Penyebab umum | Solusi |
|---|---|---|
| `ModuleNotFoundError: No module named 'x'` | package belum ter-install di kernel ini | `import sys; !{sys.executable} -m pip install x` lalu restart kernel |
| `ImportError: cannot import name 'X' from 'lib'` | beda versi library | `print(lib.__version__)`, cek dokumentasi versi itu / pakai nama lama |
| `FileNotFoundError` | path salah | `import os; os.getcwd(); os.listdir(".")`; pakai path absolut `r"C:\..."` |
| `KeyError: 'col'` | nama kolom salah (spasi, kapital) | `df.columns.tolist()`; `df.columns = df.columns.str.strip()` |
| `KeyError: "[...] not in index"` | sebagian kolom tidak ada | `[c for c in cols if c in df.columns]` |
| `ValueError: could not convert string to float` | ada teks di kolom angka | `pd.to_numeric(df[c].str.replace(",", ""), errors="coerce")` |
| `ValueError: Input contains NaN` | model sklearn tidak terima NaN | `SimpleImputer` di pipeline / `fillna` |
| `ValueError: Input contains infinity` | pembagian dengan 0 | `df.replace([np.inf, -np.inf], np.nan)` |
| `ValueError: Found input variables with inconsistent numbers of samples` | X dan y beda panjang | cek `len(X), len(y)`; jangan filter X tanpa filter y |
| `ValueError: X has N features, but model is expecting M` | kolom train ≠ test | `X_test = X_test[X_train.columns]` |
| `ValueError: Unknown label type: 'continuous'` | target float dipakai classifier | `y = y.astype(int)` atau pakai regressor |
| `ValueError: y contains previously unseen labels` | LabelEncoder ketemu kategori baru | `OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)` |
| `ValueError: Only one class present in y_true. ROC AUC score is not defined` | fold berisi 1 kelas | StratifiedKFold; data terlalu kecil |
| `TypeError: '<' not supported between 'str' and 'float'` | campuran tipe (NaN + string) saat sort/encode | `df[c] = df[c].astype(str)` atau `fillna("Missing")` |
| `TypeError: unhashable type: 'list'` | kolom berisi list/dict | ubah ke string / explode |
| `SettingWithCopyWarning` | edit slice | `df = df.copy()` sebelum edit; `df.loc[mask, c] = v` |
| `MemoryError` | data/matriks terlalu besar | sampel, `float32`, kurangi one-hot (high-card → freq encoding) |
| `IndexError: index out of bounds` | index tidak urut setelah filter | `df = df.reset_index(drop=True)` |
| `AttributeError: 'numpy.ndarray' object has no attribute 'iloc'` | tercampur numpy vs pandas | `pd.DataFrame(arr, columns=...)` atau pakai indexing numpy |
| `AttributeError: 'DataFrame' object has no attribute 'append'` | pandas ≥ 2.0 | `pd.concat([df, new])` |
| `LightGBMError: Do not support special JSON characters in feature name` | nama kolom aneh | `df.columns = df.columns.str.replace(r"[^0-9a-zA-Z_]", "_", regex=True)` |
| LightGBM `categorical_feature` mismatch | kategori train/test beda | samakan `pd.Categorical(..., categories=...)` dari gabungan train+test |
| XGBoost `DataFrame.dtypes ... must be int, float, bool or category` | kolom object | `astype("category")` + `enable_categorical=True`, atau encode |
| CatBoost `Invalid type for cat_feature ... =nan` | NaN di kolom kategori | `df[c] = df[c].fillna("NA").astype(str)` |
| CatBoost `cat_features` index error | index kolom salah | pakai nama kolom: `cat_features=[...names...]` |
| `ConvergenceWarning` (LogReg) | belum konvergen | `max_iter=5000`, scaling fitur |
| `LinAlgError: Singular matrix` (statsmodels) | kolinear / dummy trap | drop salah satu dummy (`drop_first=True`), buang fitur VIF tinggi |
| `PerfectSeparationError` | fitur memisahkan target sempurna | cek leakage; pakai regularisasi |
| `CUDA out of memory` | batch / model terlalu besar | turunkan batch, max_len/img size, fp16, model kecil; `torch.cuda.empty_cache()` |
| `RuntimeError: Expected all tensors on the same device` | sebagian tensor di CPU | `.to(device)` untuk model & batch |
| DataLoader hang di Windows | `num_workers > 0` | `num_workers=0` |
| `OSError: Can't load tokenizer/model` | tidak ada internet / nama model salah | cek nama di huggingface.co, cek koneksi |
| Plot tidak muncul | backend | `%matplotlib inline`, `plt.show()` |
| Kernel mati tiba-tiba | RAM habis | sampel data, hapus variabel besar `del x; gc.collect()` |
| Notebook lambat sekali | loop Python di DataFrame besar | vektorisasi (`np.where`, `groupby`, `.map`) |

## 3. Kebiasaan anti-error
- Setelah tiap transformasi: `print(df.shape)` dan `df.isna().sum().sum()`.
- Gabung train+test untuk preprocessing yang **tidak** memakai target (encoding kategori, parsing tanggal) supaya konsisten.
- Simpan hasil penting ke disk (`to_csv`, `to_pickle`) supaya tidak perlu run ulang dari awal.
- Satu cell = satu langkah. Kalau error, perbaiki cell itu saja.
- **Restart & Run All** sebelum submit untuk memastikan urutan cell benar.
- Gunakan `RUN_MODE="fast"` saat mengembangkan, `"full"` untuk final.

## 4. Template debugging cepat
```python
def check_df(df, name="df"):
    print(f"[{name}] shape={df.shape}")
    print("  dtypes:", df.dtypes.value_counts().to_dict())
    na = df.isna().sum(); print("  NaN cols:", na[na > 0].to_dict())
    num = df.select_dtypes("number")
    print("  inf:", int(np.isinf(num.to_numpy()).sum()))
    print("  dup rows:", int(df.duplicated().sum()))

check_df(train, "train"); check_df(test, "test")
print("kolom hanya di train:", set(train.columns) - set(test.columns))
print("kolom hanya di test :", set(test.columns) - set(train.columns))
```
