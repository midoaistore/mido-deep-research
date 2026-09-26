import streamlit as st
import requests

st.set_page_config(page_title="Mido Deep Research", page_icon="🔍", layout="wide")
st.title("🔍 Mido AI - Deep Research Agent")
st.markdown("### الوكيل البحثي اللي بيعمل تقرير كامل بالمصادر في 3 دقايق")

with st.sidebar:
    st.header("🔑 المفاتيح")
    tavily_key = st.text_input("Tavily API Key", type="password", help="جيبه مجاني من tavily.com")
    nebius_key = st.text_input("Nebius API Key (اختياري)", type="password")
    st.divider()
    st.markdown("**Mido AI Store**\n\nبيتباع بـ 299 جنيه")

query = st.text_input("❓ اسأل أي سؤال:", placeholder="مثال: ما هي احدث تقنيات الذكاء الاصطناعي في مصر 2025؟")
col1, col2 = st.columns([1,3])
with col1:
    deep = st.checkbox("بحث عميق", value=True)
with col2:
    count = st.slider("عدد المصادر", 5, 15, 8)

if st.button("🚀 ابدأ البحث العميق", type="primary", use_container_width=True):
    if not query:
        st.error("اكتب سؤالك الأول!")
    elif not tavily_key:
        st.error("حط مفتاح Tavily - مجاني من tavily.com")
    else:
        with st.status("🤖 الوكيل شغال...", expanded=True) as status:
            st.write("1️⃣ بيخطط لخطة البحث...")
            st.write(f"2️⃣ بيبحث في {count} مصادر موثوقة...")
            try:
                resp = requests.post("https://api.tavily.com/search", json={"api_key": tavily_key, "query": query, "search_depth": "advanced" if deep else "basic", "max_results": count, "include_answer": True, "include_raw_content": False}, timeout=40).json()
                results = resp.get('results', [])
                answer = resp.get('answer', '')
                st.write(f"✅ لقى {len(results)} مصدر - بيكتب التقرير...")
                
                report = f"# تقرير بحثي: {query}\n\n"
                report += f"## الملخص التنفيذي\n{answer}\n\n"
                report += "## التفاصيل من المصادر\n"
                for i, r in enumerate(results, 1):
                    report += f"\n### {i}. {r.get('title','')}\n{r.get('content','')[:600]}...\n\n**المصدر:** {r.get('url','')}\n"
                
                status.update(label="✅ التقرير جاهز!", state="complete", expanded=False)
                st.markdown(report)
                
                st.divider()
                st.download_button("📥 حمل التقرير", report, file_name="Mido_Research_Report.md")
                
                st.markdown("### 🔗 المصادر الموثوقة")
                for r in results:
                    st.link_button(r['title'][:70], r['url'])
                    
            except Exception as e:
                st.error(f"خطأ: {e} - تأكد من المفتاح")
