import translateText from './TranslationController';

const TranslationService = {
  translate: async (text, model, sourceLanguage, targetLanguage) => {
    if (!text) {
      throw new Error('Please enter text to translate.');
    }
    return await translateText(text, model, sourceLanguage, targetLanguage);
  },
};

export default TranslationService;