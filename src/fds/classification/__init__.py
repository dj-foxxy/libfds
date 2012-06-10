from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

class Feature(object):
    def __init__(self, name, klasses, training_examples):
        super(Feature, self).__init__()
        self.name = name
        self.klasses = klasses
        self.train(training_examples)

    def train(self, training_examples):
        raise NotImplementedError('subclasses must implement train.')

    def probability(self, klass, value):
        raise NotImplementedError('subclasses must implement probability.')


class BinaryFeature(Feature):
    def __repr__(self):
        return str(self)

    def __str__(self):
        klasses = []
        probabilities = []
        for klass, probability in self.distribution.iteritems():
            klasses.append(str(klass))
            probabilities.append('%.3g' % probability)
        fstr = '%%%ds  %%s' % max(len(klass) for klass in klasses)
        parts = []
        for klass, probability in zip(klasses, probabilities):
            parts.append(fstr % (klass, probability))
        return '\n'.join(parts)

    def train(self, training_examples):
        frequencies = dict((klass, {True: 0, False: 0})
                           for klass in self.klasses)

        for klass, truth in training_examples:
            frequencies[klass][truth] += 1

        self.distribution = {}

        for klass, klass_frequencies in frequencies.iteritems():
            num_training_examples = sum(klass_frequencies.itervalues())

            if num_training_examples:
                self.distribution[klass] = \
                        klass_frequencies[True] / num_training_examples
            else:
                self.distribution[klass] = float('nan')

    def probability(self, klass, truth):
        true_probability = self.distribution[klass]
        if truth:
            return true_probability
        else:
            return 1 - true_probability


class WordFeature(BinaryFeature):
    def __init__(self, word, klasses, training_examples):
        super(WordFeature, self).__init__(word, klasses, training_examples)

    @property
    def word(self):
        return self.name

    def train(self, training_examples):
        super(WordFeature, self).train((klass, self.word in words)
                                       for klass, words in training_examples)

    def probability(self, klass, words):
        return super(WordFeature, self).probability(klass, self.word in words)


class NaiveBayesClassifier(object):
    def __init__(self, klasses, features):
        super(NaiveBayesClassifier, self).__init__()
        self.klasses = klasses
        self.features = dict((feature.name, feature) for feature in features)

    def classify(self, feature_vector):
        likelihoods = {}
        for klass in self.klasses:
            for feature_name, value in feature_vector.iteritems():
                likelihoods[klass] = \
                        self.features[feature_name].probability(klass, value)
        return max(likelihoods, key=lambda klass: likelihoods[klass])


class BagOfWords(object):
    def __init__(self, klasses, dictionary, training_examples):
        super(BagOfWords, self).__init__()
        self.dictionary = dictionary
        self.preprocessor = preprocessor
        features = []
        for word in dictionary:
            features.append(WordFeature(word, klasses, training_examples))
        self._classifier = NaiveBayesClassifier(klasses, features)

    def classify(self, text):
        return self._classifier.classify(klass, text)


