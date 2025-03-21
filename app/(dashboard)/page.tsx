import { Button } from '@/components/ui/button';
import { ArrowRight, CreditCard, Database, Bot, Share2, BookHeadphones } from 'lucide-react';
import { Terminal } from './terminal';
import Image from 'next/image'

export default function HomePage() {
  return (
    <main>
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:grid lg:grid-cols-12 lg:gap-8">
            <div className="sm:text-center md:max-w-2xl md:mx-auto lg:col-span-6 lg:text-left">
              <h1 className="text-4xl font-bold text-gray-900 tracking-tight sm:text-5xl md:text-6xl">
                Create & Read Classic Works
                <span className="block text-fuchsia-500">In Chinese/English</span>
              </h1>
              <p className="mt-3 text-base text-gray-500 sm:mt-5 sm:text-xl lg:text-lg xl:text-xl">
                Create group reading sessions with a few clicks and share the text with the participants. Packed with modern AI technologies like Chinese pinyin, natural voice, and English pronounciation hints.
              </p>
              <div className="mt-8 sm:max-w-lg sm:mx-auto sm:text-center lg:text-left lg:mx-0">
                <a
                  href="https://vercel.com/templates/next.js/next-js-saas-starter"
                  target="_blank"
                >
                  <Button className="bg-white hover:bg-gray-100 text-black border border-gray-200 rounded-full text-lg px-8 py-4 inline-flex items-center justify-center mb-3 mr-3">
                    Create booklet
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                  <Button className="bg-white hover:bg-gray-100 text-black border border-gray-200 rounded-full text-lg px-8 py-4 inline-flex items-center justify-center">
                    Read classics
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </a>
              </div>
            </div>
            <div className="mt-12 relative sm:max-w-lg sm:mx-auto lg:mt-0 lg:max-w-none lg:mx-0 lg:col-span-6 lg:flex lg:items-center">
              {/* <Terminal /> */}
              <Image
                src="/images/landing_cover.jpeg"
                alt='diverse group reading books'
                width={800}
                height={500}
              />
            </div>
          </div>
        </div>
      </section>

      <section className="py-16 bg-white w-full">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:grid lg:grid-cols-3 lg:gap-8">
            <div>
              <div className="flex items-center justify-center h-12 w-12 rounded-md bg-fuchsia-500 text-white">
                <Bot className="h-6 w-6" />
              </div>
              <div className="mt-5">
                <h2 className="text-lg font-medium text-gray-900">
                  Powered by LLMs
                </h2>
                <p className="mt-2 text-base text-gray-500">
                  Leverage the power of modern LLMs for optimal reading comprehension and recall. Built-in context aware dictionary.
                </p>
              </div>
            </div>

            <div className="mt-10 lg:mt-0">
              <div className="flex items-center justify-center h-12 w-12 rounded-md bg-fuchsia-500 text-white">
                <Share2 className="h-6 w-6" />
              </div>
              <div className="mt-5">
                <h2 className="text-lg font-medium text-gray-900">
                  Make Booklets for Sharing
                </h2>
                <p className="mt-2 text-base text-gray-500">
                  Create booklets with screenshots of digital or physical books. Share with a link.
                </p>
              </div>
            </div>

            <div className="mt-10 lg:mt-0">
              <div className="flex items-center justify-center h-12 w-12 rounded-md bg-fuchsia-500 text-white">
                <BookHeadphones className="h-6 w-6" />
              </div>
              <div className="mt-5">
                <h2 className="text-lg font-medium text-gray-900">
                  Create Audio Books
                </h2>
                <p className="mt-2 text-base text-gray-500">
                  Generate AI natural voice read alongs for readers to practice pronounciation
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:grid lg:grid-cols-2 lg:gap-8 lg:items-center">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 sm:text-4xl">
                Ready to start create and read?
              </h2>
              <p className="mt-3 max-w-3xl text-lg text-gray-500">
                Our AI tools provides everything that you need to start creating booklets and learn Chinese/English through reading classic works. Focus on the words and sentences and leave the rest to us.
              </p>
            </div>
            <div className="mt-8 lg:mt-0 flex justify-center lg:justify-end">
              <a href="https://github.com/zshanhui/euthymia" target="_blank">
                <Button className="bg-white hover:bg-gray-100 text-black border border-gray-200 rounded-full text-xl px-12 py-6 inline-flex items-center justify-center">
                  We are 100% open-sourced
                  <ArrowRight className="ml-3 h-6 w-6" />
                </Button>
              </a>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
