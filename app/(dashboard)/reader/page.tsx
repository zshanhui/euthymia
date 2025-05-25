'use client';
import { useEffect, useState } from 'react';

/*
    notes on Reader

    for Chinese characters
        - segment words
        - create pinyin for each word

    for English text
*/

const englishText = `When the intelligent and animal souls are held together in one embrace, they can be kept from separating. When one gives undivided attention to the (vital) breath, and brings it to the utmost degree of pliancy, he can become as a (tender) babe. When he has cleansed away the most mysterious sights (of his imagination), he can become without a flaw. In loving the people and ruling the state, cannot he proceed without any (purpose of) action? In the opening and shutting of his gates of heaven, cannot he do so as a female bird? While his intelligence reaches in every direction, cannot he (appear to) be without knowledge? (The Dao) produces (all things) and nourishes them; it produces them and does not claim them as its own; it does all, and yet does not boast of it; it presides over all, and yet does not control them. This is what is called 'The mysterious Quality' (of the Dao).
`
const chineseText = `載營魄抱一，能無離乎？專氣致柔，能嬰兒乎？滌除玄覽，能無疵乎？愛民治國，能無知乎？天門開闔，能為雌乎？明白四達，能無知乎？生之、畜之，生而不有，為而不恃，長而不宰，是謂玄德。`

const chineseText22 = `上善若水。水善利萬物而不爭，處衆人之所惡，故幾於道。居善地，心善淵，與善仁，言善信，正善治，事善能，動善時。夫唯不爭，故無尤。`
const chineseText22Pinyin = `shàngshànruòshuǐ. shuǐ shàn lì wànwù ér bù zhēng, chù zhòngrén zhī suǒ è, gù jī yú dào. jū shàn dì, xīn shàn yuān, yǔ shàn rén, yán shàn xìn, zhèng shàn zhì, shì shàn néng, dòng shàn shí. fū wéi bù zhēng, gù wú yóu.`

const sectionDemo = {
    original: chineseText22,
    translation: englishText,
}

async function fetchTextBlockDevelopment() {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Import the text blocks
    const { textBlockDevExample } = await import('../../../lib/db/dev.data/textBlock');
    
    return textBlockDevExample;
}


export default async function ReaderView() {
    return <Reader section={sectionDemo} />
}

function Reader({ section }: { section: any }) {
  
  const [textBlocks, setTextBlocks] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchTextBlockDevelopment();
      setTextBlocks(data);
      console.log('Fetched text blocks:', data);
    };

    fetchData();
  }, []);

  return (
    <div className="max-w-prose mx-auto p-6">
      <div 
        className="text-lg leading-relaxed tracking-wide flex flex-col justify-center"
        style={{
          fontFamily: 'Inter, Noto Sans SC, sans-serif',
          wordBreak: 'break-word',
          hyphens: 'none',
          minHeight: 'calc(100vh - 12rem)' // Add minimum height for vertical centering context
        }}
      >
        {section.original.split('\n').map((paragraph: string, index: number) => (
          <p 
            key={index} 
            className="mb-4 text-foreground/90 whitespace-pre-wrap"
            style={{ textIndent: '2em' }}
          >
            {paragraph}
          </p>
        ))}
      </div>
    </div>
  );
}
