Bu proje *FastAPI* ve *Langchain* kullanılarak geliştirilmiş bir **chatbot** uygulamasıdır.
Kullanıcıların belirli bir konudaki sorularını yanıtlamak için *LLM* ve *VectorDatabase* entegrasyonu sağlar. Vector database olarak **Chroma** kullanılmıştır.

* Proje gelen soruları analiz eder, ilgili belgelerden bilgi getirir ve modelin hafızasında önceki konuşmaları tutarak tutarlı yanıtlar oluşturmasını sağlar. Ayrıca tüm istekler ve yanıtlar MSSQL veritabanında bir log tablosu oluşturularak kayıt altına alınır.

* Bu yapı **RAG** mimarisi ile çalışır ve LLM modellerinin doğruluğunu arttırmak için Chroma vector database'inden elde edilen bilgileri kullanır.

Proje çalıştırılmadan önce Chroma client'te başlatılmalıdır:
```bash
docker run -p 8001:8000 ghcr.io/chroma-core/chroma:latest
```

Bu projede kullanıcıların farklı işlemler yapabilmesi için 3 farklı FastAPI endpointi oluşturulmuştur:

### 1. /upload Endpoint
Yeni belgeleri sisteme yükleyip vectordatabase'e eklemek için kullanılır. Embedding modeli olarak `text-embedding-3-large` kullanılmıştır.


### 2. /chat Endpoint
Kullanıcının sorduğu soruya yanıt almak için kullanılır. Bu endpoint kullanıcının girdiği *session_id'ye* göre geçmiş konuşmaları hatırlayarak tutarlı ve bağlamsal olarak doğru yanıtlar sunar. LLM modeli olarak OpenAI `gpt-4o` modeli kullanılmıştır. **RAG** mimarisi kullanılarak, ilgili belgelerden alınan bilgiler *(context)* LLM'e sağlanarak modelin doğruluğu ve yanıt kalitesi arttırılır.

### 3. /collection Endpoint
Kullanıcı vector database'deki belgeleri görüntüleyebileceği bir sayfaya yönlendirilir. Chroma vector database'deki belgeleri gösteren bir [UI](https://github.com/flanker/chromadb-admin) kullanılmıştır. UI'ı çalıştırmak için:

```bash
docker run -p 3000:3000 fengzhichao/chromadb-admin
```

