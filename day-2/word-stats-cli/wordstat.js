const fs = require('fs');
const yargs = require('yargs');

// Argument parsing with yargs
const argv = yargs
  .option('file', {
    alias: 'f',
    description: 'Path to the text file',
    type: 'string',
    demandOption: true,
  })
  .option('top', {
    alias: 't',
    description: 'Top N most repeated words',
    type: 'number',
    default: 10,
  })
  .option('minLen', {
    alias: 'l',
    description: 'Minimum length of word',
    type: 'number',
    default: 1,
  })
  .option('unique', {
    alias: 'u',
    description: 'Only count unique words',
    type: 'boolean',
    default: false,
  })
  .help()
  .argv;

const processFile = (filePath) => {
  const data = fs.readFileSync(filePath, 'utf-8');
  return data.split(/\s+/).filter((word) => word.length >= argv.minLen);
};

const getStats = (words) => {
  const totalWords = words.length;
  const uniqueWords = [...new Set(words)].length;

  const wordCounts = words.reduce((acc, word) => {
    word = word.toLowerCase();
    acc[word] = (acc[word] || 0) + 1;
    return acc;
  }, {});

  const sortedWordCounts = Object.entries(wordCounts).sort(
    (a, b) => b[1] - a[1]
  );

  const topWords = sortedWordCounts.slice(0, argv.top).map(([word, count]) => ({
    word,
    count,
  }));

  const longestWord = words.reduce((longest, word) =>
    word.length > longest.length ? word : longest
  );

  const shortestWord = words.reduce((shortest, word) =>
    word.length < shortest.length ? word : shortest
  );

  return {
    totalWords,
    uniqueWords,
    longestWord,
    shortestWord,
    topWords,
  };
};

const outputStats = (stats) => {
  console.log(`Total words: ${stats.totalWords}`);
  console.log(`Unique words: ${stats.uniqueWords}`);
  console.log(`Longest word: ${stats.longestWord}`);
  console.log(`Shortest word: ${stats.shortestWord}`);
  console.log(`Top ${argv.top} most repeated words:`);
  stats.topWords.forEach((entry) => {
    console.log(`${entry.word}: ${entry.count}`);
  });
};

// Main function
const main = () => {
  const words = processFile(argv.file);

  if (argv.unique) {
    const uniqueWords = [...new Set(words)];
    outputStats(getStats(uniqueWords));
  } else {
    outputStats(getStats(words));
  }
};

main();
