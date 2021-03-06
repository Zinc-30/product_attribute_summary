import math
import numpy as np


def precision_at_k_per_record(actual, predicted, topk):
    if len(predicted)>topk:
        predicted = predicted[:topk]
    act_set = set(actual)
    pred_set = set(predicted)

    return len(act_set & pred_set) / float(len(pred_set))

def precision_at_k_batch(actual, predicted, topk):
    sum_precision = 0.0
    num_records = len(predicted)
    for i in range(num_records):
        sum_precision += precision_at_k_per_record(actual[i], predicted[i], topk)

    return sum_precision / num_records

def recall_at_k_per_record(actual, predicted, topk):
    if len(predicted)>topk:
        predicted = predicted[:topk]
    act_set = set(actual)
    pred_set = set(predicted)

    return len(act_set & pred_set) / float(len(act_set))

def recall_at_k_batch(actual, predicted, topk):
    sum_recall = 0.0
    num_records = len(predicted)
    for i in range(num_records):
        sum_recall += recall_at_k_per_record(actual[i], predicted[i], topk)
            
    return sum_recall / num_records

def idcg_k(k):
    res = sum([1.0/math.log(i+2, 2) for i in range(k)])
    if not res:
        return 1.0
    else:
        return res

def ndcg_k_per_record(actual, predicted, topk):
    k = min(topk, len(actual))
    idcg = idcg_k(k)
    dcg_k = sum([int(predicted[j] in set(actual))/math.log(j+2,2) for j in range(topk)])

    return dcg_k / idcg

def ndcg_k_batch(actual, predicted, topk):
    res = 0
    for record_id in range(len(actual)):
        res += ndcg_k_per_record(actual[record_id], predicted[record_id], topk)
        
    return res / float(len(actual))





def to_lowercase(input_list):                  # Convert all keyphrase to lower case
    for i, s in enumerate(input_list):
        input_list[i] = s.lower()
    return input_list


def f1_at_k_per_record(actual, predicted, topk):  # F1 Score for one document
    actual = to_lowercase(actual)
    predicted = to_lowercase(predicted)
    precision = precision_at_k_per_record(actual, predicted, topk)
    recall = recall_at_k_per_record(actual, predicted, topk)
    if precision + recall == 0:
        return 0.0
    else:
        return 2 * precision * recall / (precision + recall)


def f1_at_k_batch(actual, predicted, topk):     # Average F1 Score for all documents
    sum_f1 = 0.0
    num_records = len(predicted)
    for i in range(num_records):
        sum_f1 += f1_at_k_per_record(actual[i], predicted[i], topk)
    return sum_f1 / num_records


def bpref(gt_list, pred_list, topk=None):   # Binary Preference Measure 
    gt_list = to_lowercase(gt_list)
    pred_list = to_lowercase(pred_list)
    if isinstance(pred_list[0], list):
        doc_bpref = []
        for doc in pred_list:
            non_ingt, s, r = 0, 0, 0
            if topk == None:
                topk = len(doc)
            for idx, keyphrase in enumerate(doc, start=1):
                if idx > topk:
                    break
                if keyphrase in gt_list:
                    s += 1 - non_ingt / topk
                    r += 1
                else:
                    non_ingt += 1
            if r != 0:
                doc_bpref.append(s / r)
            else:
                doc_bpref.append(0.0)
        return np.mean(doc_bpref)
    else:
        non_ingt, s, r = 0, 0, 0
        if topk == None:
            topk = len(pred_list)
        for idx, keyphrase in enumerate(pred_list, start=1):
            if idx > topk:
                break
            elif keyphrase in gt_list:
                s += 1 - non_ingt / topk
                r += 1
            else:
                non_ingt += 1
        if r != 0:
            return s / r
        else:
            return 0.0

        
def map(gt_list, pred_list, topk=None):   # Mean Average Precision
    total_precision = []
    gt_list = to_lowercase(gt_list)
    pred_list = to_lowercase(pred_list)
    if isinstance(pred_list[0], list):
        for doc in pred_list:
            if topk == None:
                topk = len(doc)
            count = 0
            doc_precision = []
            for idx, keyphrase in enumerate(doc, start=1):
                if idx > topk:
                    break
                elif keyphrase in gt_list:
                    count += 1
                    doc_precision.append(count / idx)
            if doc_precision:
                mean_doc_precision = np.mean(doc_precision)
            else:
                mean_doc_precision = 0.0
            total_precision.append(mean_doc_precision)
    else:
        count = 0
        if topk == None:
            topk = len(pred_list)
        for idx, keyphrase in enumerate(pred_list, start=1):
            if idx > topk:
                break
            elif keyphrase in gt_list:
                count += 1
                total_precision.append(count / idx)
        if not total_precision:
            total_precision.append(0.0)
    return np.mean(total_precision)


def mrr(gt_list, pred_list):     # Mean Reciprocal Rank
    s = 0
    gt_list = to_lowercase(gt_list)
    pred_list = to_lowercase(pred_list)
    if isinstance(pred_list[0], list):
        d = len(pred_list)
        for doc in pred_list:
            for idx, keyphrase in enumerate(doc, start=1):
                if keyphrase in gt_list:
                    s += 1 / idx
                    break
    else:
        d = 1
        for idx, keyphrase in enumerate(pred_list, start=1):
            if keyphrase in gt_list:
                s += 1 / idx
                break
    return s / d

if __name__=='__main__':
    src = ["hello word","test data","computer game","west wood","greet game","good video games"]
    tgt = ["test data","computer game","worth money", "cheap books","funny item"]
    print(ndcg_k_batch(src,tgt,2))
