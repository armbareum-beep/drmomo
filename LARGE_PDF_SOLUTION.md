# 큰 PDF 파일 처리 - 실용적 해결책

## 🚨 문제점

**Ettinger 교과서 (255MB, 수천 페이지)**가 너무 커서:
- 로딩에 매우 오래 걸림 (5-10분 이상)
- 메모리 많이 사용
- 임베딩 생성 비용 높음 (OpenAI API 비용)

## ✅ 권장 해결책

### 방법 1: 선택적 로딩 (가장 실용적) ⭐

필요한 파일만 documents 폴더에 넣기:

```bash
# 작은 파일만 사용
documents/
  ├── veterinary_guide.pdf (테스트용)
  ├── handbook_radiology.pdf (15MB - OK)
  └── emergency_protocols.pdf (작은 파일들)

# 큰 파일은 백업에 보관
documents_backup/
  └── Ettinger_Textbook.pdf (255MB - 너무 큼)
```

### 방법 2: PDF 분할 도구 사용

**온라인 도구:**
- https://www.ilovepdf.com/split_pdf
- https://smallpdf.com/split-pdf

**방법:**
1. Ettinger 교과서를 챕터별로 분할
2. 필요한 챕터만 documents에 추가
   - 예: `ettinger_ch10_gastro.pdf`
   - 예: `ettinger_ch15_cardio.pdf`

### 방법 3: 벡터 DB 캐싱 (고급)

한 번만 처리하고 저장:

```python
# app.py에 추가
import os

CACHE_DIR = "vectorstore_cache"

def initialize_rag_system():
    global qa_chain
    
    # 캐시 확인
    if os.path.exists(CACHE_DIR):
        print("📦 Loading from cache...")
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.load_local(CACHE_DIR, embeddings)
    else:
        print("📂 Processing documents (first time only)...")
        vectorstore = load_and_process_documents(folder_path="documents")
        # 캐시 저장
        vectorstore.save_local(CACHE_DIR)
        print("💾 Saved to cache for next time!")
    
    qa_chain = create_rag_chain(vectorstore)
```

---

## 💡 즉시 사용 가능한 방법

### 옵션 A: 작은 파일만 사용
```bash
# Ettinger 제거
move documents\"Ettinger's Textbook*.pdf" documents_backup\

# 서버 재시작
python app.py
```

### 옵션 B: 하나씩 추가
```bash
# 필요한 파일만 추가
copy documents_backup\handbook*.pdf documents\

# 서버 재시작하고 테스트
python app.py
```

---

## 📊 파일 크기별 예상 시간

| 파일 크기 | 로딩 시간 | 임베딩 시간 | 총 시간 |
|----------|----------|------------|--------|
| < 10MB   | 10초     | 30초       | ~1분   |
| 10-50MB  | 30초     | 2분        | ~3분   |
| 50-100MB | 1분      | 5분        | ~6분   |
| 100MB+   | 2-5분    | 10-20분    | 15-25분 |

**Ettinger (255MB)**: 예상 30-60분 😱

---

## 🎯 추천 전략

1. **지금 당장**: 작은 파일들만 사용 (Handbook만)
2. **단기**: 필요한 챕터만 PDF 분할해서 추가
3. **장기**: 벡터 DB 캐싱 구현

어떤 방법을 선택하시겠어요?
