# 큰 PDF 파일 처리 가이드

## 문제 해결 방법

### 1️⃣ 개선된 에러 처리 (방금 적용됨)
- ✅ 문제있는 파일은 건너뛰고 계속 진행
- ✅ 진행상황 표시
- ✅ 성공/실패 파일 목록 표시

### 2️⃣ 백업 파일 다시 추가하기

큰 파일들을 하나씩 추가해보세요:

```bash
# 하나씩 테스트
copy documents_backup\*.pdf documents\
```

서버를 재시작하면 자동으로 로드됩니다.

### 3️⃣ PDF 최적화 (권장)

#### 방법 A: PDF 압축
- Adobe Acrobat 또는 온라인 도구 사용
- 이미지 품질 낮추기
- 불필요한 메타데이터 제거

#### 방법 B: 챕터별 분할
큰 교과서를 챕터별로 나누기:
- PDF 편집 도구 사용
- 각 챕터를 별도 파일로 저장
- 예: `ettinger_chapter1.pdf`, `ettinger_chapter2.pdf`

#### 방법 C: 텍스트 추출
- PDF에서 텍스트만 추출
- `.txt` 파일로 저장
- 훨씬 빠르게 로드됨

### 4️⃣ 벡터 DB 저장 (고급)

한 번 처리한 후 저장해두면 다음엔 빠르게 로드:

```python
# vectorstore 저장
vectorstore.save_local("vectorstore_cache")

# 다음 실행 시 로드
vectorstore = FAISS.load_local("vectorstore_cache", embeddings)
```

### 5️⃣ 청크 크기 조정

매우 큰 파일의 경우:

```python
# rag_system.py에서
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # 더 작게 (기본: 1000)
    chunk_overlap=50  # 더 작게 (기본: 150)
)
```

---

## 추천 방법

**단기 해결책:**
1. 개선된 시스템으로 백업 파일 다시 추가
2. 에러 나는 파일만 제외

**장기 해결책:**
1. PDF를 챕터별로 분할
2. 벡터 DB 캐싱 구현
3. 전용 서버에서 실행 (더 많은 메모리)

---

## 테스트해보기

지금 바로 백업 파일을 추가해볼까요?
