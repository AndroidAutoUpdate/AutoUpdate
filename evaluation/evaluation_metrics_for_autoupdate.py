# -*- coding:utf-8 -*-
import argparse
import bleu
import weighted_ngram_match
import syntax_match
import dataflow_match
import numpy as np
import sys

def compare_with_groud_truth_from_path(prediction_p, ground_truth_p):
    predictions = [x.strip() for x in open(prediction_p, 'r', encoding='utf-8').readlines()]
    ground_truths = [x.strip() for x in open(ground_truth_p, 'r', encoding='utf-8').readlines()]
    return compare_with_groud_truth(predictions, ground_truths)

def compare_with_groud_truth(predictions, ground_truths):
    count = 0
    if len(predictions)==len(ground_truths):
        for i in range(len(predictions)):
            correct_after = ground_truths[i].strip()
            beams = predictions[i].split('\t')
            for b in beams:
                pred = b.strip()

                if pred == correct_after:
                    count = count + 1
                    break

    return count, len(predictions)


def compute_code_bleu_from_path(prediction_p, references_p, beam_size):
    hypothesis = [x.strip() for x in open(prediction_p, 'r', encoding='utf-8').readlines()]
    pre_references = [x.strip() for x in open(references_p, 'r', encoding='utf-8').readlines()]

    return compute_code_bleu(hypothesis, pre_references, beam_size)

def compute_code_bleu(hypothesis, pre_references, beam_size):
    alpha,beta,gamma,theta  = 0.25,0.25,0.25,0.25
    lang = 'java'
    
    all_hypothesis = []
    for i in range(beam_size):
        all_hypothesis.append([])
        
    for methods in hypothesis:
        methods = methods.split('\t')
        for j in range(beam_size):
            if j < len(methods):
                all_hypothesis[j].append(methods[j])
            else:
                all_hypothesis[j].append(" ")

    ngram_match_score_S, weighted_ngram_match_score_S, syntax_match_score_S, dataflow_match_score_S = [],[],[],[]
    for i in range(beam_size):
        references = pre_references
        hypothesis = all_hypothesis[i]
        tokenized_hyps = [x.split() for x in hypothesis]
        tokenized_refs = [[x.split()] for x in pre_references]
        references = [[x] for x in references]
        
        # calculate ngram match (BLEU)
        ngram_match_score = bleu.corpus_bleu(tokenized_refs,tokenized_hyps)
                
        
        # calculate weighted ngram match
        keywords = [x.strip() for x in open('keywords/'+lang+'.txt', 'r', encoding='utf-8').readlines()]
        def make_weights(reference_tokens, key_word_list):
            return {token:1 if token in key_word_list else 0.2 \
                    for token in reference_tokens}
        tokenized_refs_with_weights = [[[reference_tokens, make_weights(reference_tokens, keywords)]\
                    for reference_tokens in reference] for reference in tokenized_refs]
        weighted_ngram_match_score = weighted_ngram_match.corpus_bleu(tokenized_refs_with_weights,tokenized_hyps)
    
        # calculate syntax match
        syntax_match_score = syntax_match.corpus_syntax_match(references, hypothesis, lang)
        #print(syntax_match_score)

        # calculate dataflow match
        dataflow_match_score = dataflow_match.corpus_dataflow_match(references, hypothesis, lang)  
        
        ngram_match_score_S.append(ngram_match_score)
        weighted_ngram_match_score_S.append(weighted_ngram_match_score)
        syntax_match_score_S.append(syntax_match_score)
        dataflow_match_score_S.append(dataflow_match_score)

    ngram_match_score = np.max(np.array(ngram_match_score_S))
    weighted_ngram_match_score = np.max(np.array(weighted_ngram_match_score_S))
    syntax_match_score = np.max(np.array(syntax_match_score_S))
    dataflow_match_score = np.max(np.array(dataflow_match_score))
    code_bleu = alpha*ngram_match_score\
                + beta*weighted_ngram_match_score\
                + gamma*syntax_match_score\
                + theta*dataflow_match_score
    return  ngram_match_score, code_bleu


if __name__ == '__main__':
    decode_prediction_path = sys.argv[1]
    reference_path = sys.argv[2]
    beam_size = sys.argv[3]
    correct_count, total = compare_with_groud_truth_from_path(decode_prediction_path, reference_path)
    bleu, code_bleu = compute_code_bleu_from_path(decode_prediction_path, reference_path, int(beam_size))
    print(beam_size,correct_count, total, correct_count/total, code_bleu)    
