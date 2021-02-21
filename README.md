python版本为3.6.7\
第一部分：各个文件介绍\
1、bert_base文件夹:google官方bert的源代码\
2、model_deploy_NER文件夹：模型训练完成后,运行run_server.py生成的模型部署pb文件在output文件夹，需要手动拷贝到此文件夹\
3、client文件夹：模型部署后给客户端调用的接口文件\
4、NERdata文件夹：模型训练数据集,放了少量的数据方便对战数据结构，实际训练数据来自大概10万条文本数据，构造成40多万条样本，通过标点符号划分构造成样本，大小200M左右的数据集，一共2个实体大类，位置和购买方\
5、NERdata_origin文件夹：模型训练原始文本数据集，放了少量的数据方便对战数据结构\
6、output文件夹：运行run.py后存储训练完成的模型文件，以及运行run_server.py生成模型部署pb文件也存在这个文件夹\
7、roeberta_zh_L-12_H-768_A-12文件夹：google开源的中文预训练模型\
8、client_test.py文件：模型部署后给客户端调用的接口文件\
9、generate_train_data.py文件：运行此文件把原始数据的文本数据生成训练样本数据\
10、README.md文件：说明介绍文件\
11、requirements文件：项目运行的环境打包说明\
12、run.py文件：训练模型直接运行此文件\
13、run_server.py文件：模型训练完成后运行此文件可以生成模型部署文件\
14、terminal_predict.py：模型训练完成后运行此文件可以本地测试模型效果

第二部分：训练模型\
1、运行generate_train_data.py文件，根据NERdata_origin文件夹原始数据格式，生成模型训练样本数据存放在NERdata文件夹，可直接参照格式改成自己的数据
2、下载预训练模型，网盘链接：https://pan.baidu.com/s/1yPD5sf-3c4iE-7zrkg-UYg 提取码：5d5e ，解压后把文件夹里面的ckpt等预训练文件放在工程的roeberta_zh_L-12_H-768_A-12文件夹\
3、安装工程运行环境，打开终端一键运行安装 pip install -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com -r requirement.txt\
4、运行run.py模型训练，超参数配置如下，也可以按需求把data文件夹的数据按一样的格式换成自己的数据，训练完的模型在工程的output文件夹
5、运行run_classifier.py模型训练，超参数配置如下，也可以按需求把data文件夹的数据按一样的格式换成自己的数据，训练完的模型在工程的output_model文件夹\
5.0、训练:\
python run.py\
-data_dir=NERdata\
-output_dir=output\
-init_checkpoint=roeberta_zh_L-12_H-768_A-12/bert_model.ckpt\
-bert_config_file=roeberta_zh_L-12_H-768_A-12/bert_config.json\
-vocab_file=roeberta_zh_L-12_H-768_A-12/vocab.txt\
-batch_size=4\
-max_seq_length=420\
-num_train_epochs=3.0\
-learning_rate=2e-5\
6、最终模型的准确率如下\
processed 5387936 tokens with 44791 phrases; found: 44285 phrases; correct: 43662.\
accuracy:  99.88%; precision:  98.59%; recall:  97.48%; FB1:  98.03\
              LOC: precision:  98.42%; recall:  98.40%; FB1:  98.41  22424\
              ORG: precision:  98.77%; recall:  96.56%; FB1:  97.65  21861
              
第三部分：本地win10系统部署和调用模型\
1、运行
run_server.py \
-mode=NER\
-bert_model_dir=roeberta_zh_L-12_H-768_A-12\
-model_dir=output\
-model_pb_dir=output\
-max_seq_len=420\
2、以上代码运行后没有报错，部署成功后可以运行client_test.py文件进行模型调用，默认的地址是本地部署地址

第四部分：linux服务器部署和调用模型\
1、运行
run_server.py \
-mode=NER\
-bert_model_dir=roeberta_zh_L-12_H-768_A-12\
-model_dir=output\
-model_pb_dir=output\
-max_seq_len=420\
2、将output文件夹里面生成的模型pb文件拷贝到model_deploy_NER文件夹\
3、把model_deploy_NER文件压缩后，通过rz指令上传到服务器，然后通过unzip解压，通过rm删除多余的文件，通过ls查看当前目录文件，通过pwd查看当前目录 注意切换虚拟环境，选择虚拟环境，服务器一定是python3，默认python是python2的，一定要做好运行区分\
python3 run.py -bert_model_dir=/home/mart/model_deploy_NER/roeberta_zh_L-12_H-768_A-12 -model_dir=/home/mart/model_deploy_NER/output -model_pb_dir=/home/mart/model_deploy_NER/output -mode=NER -max_seq_len=420 -port=5755 -port_out=5756 -http_port=5758，注意文件夹的绝对路径改成和自己的一致\
4、以上代码运行后没有报错，部署成功后可以运行client_test.py文件进行模型调用，默认的地址是本地部署地址,把IP改成服务器的IP即可直接调用