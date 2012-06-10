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
    def __init__(self, name, klasses, training_examples, smoothing=0):
        self.smoothing = smoothing
        super(BinaryFeature, self).__init__(name, klasses, training_examples)

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
        frequencies = dict((klass, {True: self.smoothing,
                                    False: self.smoothing})
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


class NaiveBayesClassifier(object):
    def __init__(self, klasses, features):
        super(NaiveBayesClassifier, self).__init__()
        self.klasses = klasses
        self.features = dict((feature.name, feature) for feature in features)

    def __str__(self):
        return '\n\n'.join('%s\n%s' % (name, feature)
                           for name, feature in self.features.iteritems())

    def classify(self, observation):
        likelihoods = {}
        for klass in self.klasses:
            likelihoods[klass] = 1
            for name, feature in self.features.iteritems():
                likelihoods[klass] *= feature.probability(klass,
                                                          observation[name])
        return max(likelihoods, key=lambda klass: likelihoods[klass])


class BagOfWords(object):
    def __init__(self, klasses, dictionary, training_examples, smoothing=0):
        super(BagOfWords, self).__init__()
        self.dictionary = dictionary

        features = []
        for word in dictionary:
            features.append(
                    BinaryFeature(word, klasses,
                                  ((klass, word in words)
                                   for klass, words in training_examples),
                                  smoothing=smoothing))

        self._classifier = NaiveBayesClassifier(klasses, features)

    def __str__(self):
        return str(self._classifier)

    def classify(self, text):
        return self._classifier.classify(dict((word, word in text)
                                              for word in self.dictionary))


