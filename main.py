import asyncio

from time import perf_counter

from zoey import Core
        
async def main():
    # How to use
    start = perf_counter()
    core = Core()
    tasks = []
    questions = [
        "Kamu cantik banget :)",
        "Bisakah kamu membantuku mengerjakan tugas?",
        "Siapa pemain bola terbaik di seluruh dunia menurut kamu?",
        "Rating film blade runner in a scale 1 to 100", "Apa itu black hole?",
        "Ceritakan tentang sejarah Indonesia secara singkat.",
        "Bagaimana cara membuat API dengan FastAPI?",
        "Mengapa langit berwarna biru?",
        "Apa perbedaan antara AI dan Machine Learning?",
        "Buatkan saya puisi pendek tentang hujan.",
        "Kenapa kucing suka mengeong saat lapar?",
        "Bagaimana cara deploy FastAPI ke Vercel?",
        "Apa keunggulan Python dibanding bahasa lain?",
        "Siapa tokoh penting dalam sejarah teknologi dunia?",
        "Bagaimana cara kerja blockchain?",
        "Apakah mungkin AI memiliki kesadaran?",
        "Jelaskan konsep Internet of Things (IoT).",
        "Bagaimana prediksi cuaca dilakukan dengan AI?",
        "Apa arti dari kata 'serendipity'?",
        "Tolong buatkan saya list resolusi tahun baru.",
        "Apa film terbaik sepanjang masa menurutmu?",
        "Bagaimana AI dapat digunakan dalam bidang pendidikan?",
        "Tuliskan definisi sederhana tentang quantum computing.",
        "Apa itu Metaverse dan dampaknya bagi masa depan?"
    ]
    for item in questions:
        tasks.append(core.generate_response(item))
    responses = await asyncio.gather(*tasks)
    for item in responses:
        print(item)
    await core.close_session()
    print(f"Time: {perf_counter() - start}")

if __name__ == "__main__":
    asyncio.run(main())