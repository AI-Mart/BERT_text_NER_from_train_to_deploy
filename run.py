#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
模型训练文件函数
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

########指定GPU运行
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"


########指定CPU运行
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"



def start_server():
    from bert_base.server import BertServer
    from bert_base.server.helper import get_run_args

    args = get_run_args()
    print(args)
    server = BertServer(args)
    server.start()
    server.join()


def train_ner():
    import os
    from bert_base.train.train_helper import get_args_parser
    from bert_base.train.bert_lstm_ner import train

    args = get_args_parser()
    if True:
        import sys
        param_str = '\n'.join(['%20s = %s' % (k, v) for k, v in sorted(vars(args).items())])
        print('usage: %s\n%20s   %s\n%s\n%s\n' % (' '.join(sys.argv), 'ARG', 'VALUE', '_' * 50, param_str))
    print(args)
    os.environ['CUDA_VISIBLE_DEVICES'] = args.device_map
    train(args=args)


if __name__ == '__main__':
    """
    如果想训练，那么直接 指定参数跑，如果想启动服务，那么注释掉train,打开server即可
    """
    train_ner()
    # start_server()