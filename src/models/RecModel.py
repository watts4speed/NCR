# coding=utf-8

import torch
import torch.nn.functional as F
from src.models.BaseModel import BaseModel
from src.utils import utils


class RecModel(BaseModel):
    append_id = True
    include_id = False
    include_user_features = False
    include_item_features = False

    @staticmethod
    def parse_model_args(parser, model_name='RecModel'):
        parser.add_argument('--u_vector_size', type=int, default=64,
                            help='Size of user vectors.')
        parser.add_argument('--i_vector_size', type=int, default=64,
                            help='Size of item vectors.')
        return BaseModel.parse_model_args(parser, model_name)

    def __init__(self, label_min, label_max, feature_num, user_num, item_num, u_vector_size, i_vector_size,
                 random_seed, model_path):
        self.u_vector_size, self.i_vector_size = u_vector_size, i_vector_size
        assert self.u_vector_size == self.i_vector_size
        self.ui_vector_size = self.u_vector_size
        self.user_num = user_num
        self.item_num = item_num
        BaseModel.__init__(self, label_min=label_min, label_max=label_max,
                           feature_num=feature_num, random_seed=random_seed,
                           model_path=model_path)

    def _init_weights(self):
        self.uid_embeddings = torch.nn.Embedding(self.user_num, self.ui_vector_size)
        self.iid_embeddings = torch.nn.Embedding(self.item_num, self.ui_vector_size)

    def predict(self, feed_dict):
        check_list = []
        u_ids = feed_dict['X'][:, 0]
        i_ids = feed_dict['X'][:, 1]

        cf_u_vectors = self.uid_embeddings(u_ids)
        cf_i_vectors = self.iid_embeddings(i_ids)
        prediction = (cf_u_vectors * cf_i_vectors).sum(dim=1).view([-1])
        out_dict = {'prediction': prediction,
                    'check': check_list}
        return out_dict

