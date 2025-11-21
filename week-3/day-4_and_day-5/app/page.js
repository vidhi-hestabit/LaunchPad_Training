import Image from "next/image";

export const metadata = {
  title: "Capstone project - Week-3",
};

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-background text-foreground">

      <section className="px-6 py-20 text-center">
        <span className="inline-block mb-4 px-4 py-1 bg-blue-100 text-blue-600 rounded-full text-sm font-medium animate-fadeLoop">
          Software Engineer Trainee @ HestaBit
        </span>
        <h1 className="text-4xl md:text-6xl font-bold max-w-4xl mx-auto leading-tight animate-pulseSlow">
          Capstone Mini <span className="text-blue-600"> Project </span> Week-3 
        </h1>
        <p className="text-gray-600 max-w-2xl mx-auto mt-6 text-lg md:text-xl animate-fadeLoop">
          Learning and creating innovative solutions using React, Next.js, and Tailwind CSS.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8">
          <button className="px-8 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition">
            View My Work
          </button>

          <button className="px-8 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:border-blue-600 hover:text-blue-600 transition">
            Contact Me
          </button>
        </div>

        <div className="mt-16 max-w-5xl mx-auto animate-float">
          <Image src="https://assets.startbootstrap.com/img/meta/products/twitter/twitter-image-sb-admin.png" alt="Modern Dashboard Interface" width={1200} height={630} 
          className="rounded-2xl shadow-lg border" />
        </div>
      </section>

      <section className="px-6 py-20 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4 animate-pulseSlow">
            Technical Skills
          </h2>
          <p className="text-gray-600 text-center max-w-2xl mx-auto mb-12 animate-fadeLoop">
            Technologies I'm working with at HestaBit Technologies.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                icon: "⚛️",
                title: "Next.js",
                desc: "Building modern web apps with SSR and routing.",
              },
              {
                icon: "🎨",
                title: "UI/UX Design",
                desc: "Creating responsive UI with Tailwind CSS.",
              },
              {
                icon: "⚡",
                title: "Optimization",
                desc: "Improving performance & SEO.",
              },
            ].map((item, i) => (
              <div
                key={i}
                className="p-8 bg-gray-50 rounded-2xl shadow-md border hover:shadow-xl transition animate-cardWave"
                style={{ animationDelay: `${i * 0.3}s` }}
              >
                <div className="text-4xl mb-4">{item.icon}</div>
                <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
                <p className="text-gray-600">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="px-6 py-20">
        <div className="max-w-6xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 animate-pulseSlow"> My Learning</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {["Dynamic Routing", "UI Library", "Landing Page"].map(
              (title, i) => (
                <div
                  key={i}
                  className="bg-white p-6 rounded-xl shadow-md border hover:shadow-xl transition animate-cardWave"
                  style={{ animationDelay: `${i * 0.2}s` }} >
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                    <span className="text-blue-600 text-lg font-bold">
                      {i + 1}
                    </span>
                  </div>
                  <h3 className="text-xl font-semibold mb-2">{title}</h3>
                  <p className="text-gray-600">
                    Built using best practices in Next.js.
                  </p>
                </div>
              )
            )}
          </div>
        </div>
      </section>

      <section className="px-6 py-20 bg-gray-50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 animate-pulseSlow">
            Let's Connect
          </h2>
          <p className="text-gray-600 mb-8 animate-fadeLoop">
            Interested in collaborating or discussing development topics?
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="mailto:your.email@hestabit.com" className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
              Send Email
            </a>
            <a href="#" className="px-8 py-3 border border-gray-300 text-gray-700 rounded-lg hover:border-blue-600 hover:text-blue-600 transition">
              LinkedIn
            </a>
          </div>
        </div>
      </section>

      <footer className="bg-gray-900 text-gray-400 py-8 text-center">
        <p>© 2025 Software Engineer Trainee @ HestaBit Technologies</p>
      </footer>
    </main>
  );
}
