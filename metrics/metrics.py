import math


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

