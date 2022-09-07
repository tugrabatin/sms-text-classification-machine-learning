{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "fcc_sms_text_classification.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/a-mt/fcc-sms-text-classification/blob/main/fcc_sms_text_classification.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "Eg62Pmz3o83v"
      },
      "source": [
        "## Instructions\n",
        "\n",
        "In this challenge, you need to create a machine learning model that will classify SMS messages as either \"ham\" or \"spam\". A \"ham\" message is a normal message sent by a friend. A \"spam\" message is an advertisement or a message sent by a company.\n",
        "\n",
        "You should create a function called `predict_message` that takes a message string as an argument and returns a list. The first element in the list should be a number between zero and one that indicates the likeliness of \"ham\" (0) or \"spam\" (1). The second element in the list should be the word \"ham\" or \"spam\", depending on which is most likely.\n",
        "\n",
        "For this challenge, you will use the [SMS Spam Collection dataset](http://www.dt.fee.unicamp.br/~tiago/smsspamcollection/). The dataset has already been grouped into train data and test data.\n",
        "\n",
        "The first two cells import the libraries and data. The final cell tests your model and function. Add your code in between these cells.\n",
        "\n",
        "## Load libraries\n"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "8RZOuS9LWQvv",
        "outputId": "8a737f80-8f4c-42ed-8ae4-7e36a81db5b6",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "import numpy as np\n",
        "import pandas as pd\n",
        "import matplotlib.pyplot as plt\n",
        "import tensorflow as tf\n",
        "\n",
        "print(tf.__version__)"
      ],
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "2.3.0\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "dnRdBxHgd_qZ"
      },
      "source": [
        "## Load dataset"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "lMHwYXHXCar3"
      },
      "source": [
        "# get data files\n",
        "TRAIN_DATA_URL = \"https://raw.githubusercontent.com/beaucarnes/fcc_python_curriculum/master/sms/train-data.tsv\"\n",
        "TEST_DATA_URL  = \"https://raw.githubusercontent.com/beaucarnes/fcc_python_curriculum/master/sms/valid-data.tsv\"\n",
        "\n",
        "train_file_path = tf.keras.utils.get_file(\"train-data.tsv\", TRAIN_DATA_URL)\n",
        "test_file_path  = tf.keras.utils.get_file(\"valid-data.tsv\", TEST_DATA_URL)"
      ],
      "execution_count": 3,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "8v0FkE4meWfP",
        "outputId": "dfd58740-a3bf-4928-d09d-7ceae1034f6b",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 52
        }
      },
      "source": [
        "print(train_file_path)\n",
        "print(test_file_path)"
      ],
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "/root/.keras/datasets/train-data.tsv\n",
            "/root/.keras/datasets/valid-data.tsv\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "g_h508FEClxO",
        "outputId": "319b3602-52c0-4ca6-90d2-aaf86227d08f",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 206
        }
      },
      "source": [
        "df_train = pd.read_csv(train_file_path, sep=\"\\t\", header=None, names=['y', 'x'])\n",
        "df_train.head()"
      ],
      "execution_count": 5,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>y</th>\n",
              "      <th>x</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>ham</td>\n",
              "      <td>ahhhh...just woken up!had a bad dream about u ...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>ham</td>\n",
              "      <td>you can never do nothing</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>ham</td>\n",
              "      <td>now u sound like manky scouse boy steve,like! ...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>ham</td>\n",
              "      <td>mum say we wan to go then go... then she can s...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>ham</td>\n",
              "      <td>never y lei... i v lazy... got wat? dat day ü ...</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "     y                                                  x\n",
              "0  ham  ahhhh...just woken up!had a bad dream about u ...\n",
              "1  ham                           you can never do nothing\n",
              "2  ham  now u sound like manky scouse boy steve,like! ...\n",
              "3  ham  mum say we wan to go then go... then she can s...\n",
              "4  ham  never y lei... i v lazy... got wat? dat day ü ..."
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 5
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "zOMKywn4zReN",
        "outputId": "38d521b9-1a49-4c23-e097-d3f820abf25f",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 206
        }
      },
      "source": [
        "df_test = pd.read_csv(test_file_path, sep=\"\\t\", header=None, names=['y', 'x'])\n",
        "df_test.head()"
      ],
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>y</th>\n",
              "      <th>x</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>ham</td>\n",
              "      <td>i am in hospital da. . i will return home in e...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>ham</td>\n",
              "      <td>not much, just some textin'. how bout you?</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>ham</td>\n",
              "      <td>i probably won't eat at all today. i think i'm...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>ham</td>\n",
              "      <td>don‘t give a flying monkeys wot they think and...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>ham</td>\n",
              "      <td>who are you seeing?</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "     y                                                  x\n",
              "0  ham  i am in hospital da. . i will return home in e...\n",
              "1  ham         not much, just some textin'. how bout you?\n",
              "2  ham  i probably won't eat at all today. i think i'm...\n",
              "3  ham  don‘t give a flying monkeys wot they think and...\n",
              "4  ham                                who are you seeing?"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 6
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "2ZYXChVZe0Zu",
        "outputId": "46a2f90e-d476-42c0-e158-ae19d0d95a33",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 52
        }
      },
      "source": [
        "print(len(df_train))\n",
        "print(len(df_test))"
      ],
      "execution_count": 7,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "4179\n",
            "1392\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "oXzj_dWIoWbr"
      },
      "source": [
        "## Handle categorical values"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "R7gxxCoAod0Y",
        "outputId": "5207b5c9-45ae-44ba-ff22-edcc86df9ee7",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 121
        }
      },
      "source": [
        "y_train = df_train['y'].astype('category').cat.codes\n",
        "y_test  = df_test['y'].astype('category').cat.codes\n",
        "y_train[:5]"
      ],
      "execution_count": 8,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "0    0\n",
              "1    0\n",
              "2    0\n",
              "3    0\n",
              "4    0\n",
              "dtype: int8"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 8
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "5mzVab6gzUKK",
        "outputId": "37860dfc-65c9-4d22-8935-82afa3f453fd",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 312
        }
      },
      "source": [
        "bar = df_train['y'].value_counts()\n",
        "\n",
        "plt.bar(bar.index, bar)\n",
        "plt.xlabel('Label')\n",
        "plt.title('Number of ham and spam messages')"
      ],
      "execution_count": 9,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "Text(0.5, 1.0, 'Number of ham and spam messages')"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 9
        },
        {
          "output_type": "display_data",
          "data": {
            "image/png": "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\n",
            "text/plain": [
              "<Figure size 432x288 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": [],
            "needs_background": "light"
          }
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "JpjaMZjZg0hj"
      },
      "source": [
        "## Text preprocessing"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "pJ_0diidk_Br",
        "outputId": "c99bfcde-8bd0-4339-a082-509c5b63a1e4",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 104
        }
      },
      "source": [
        "import nltk\n",
        "nltk.download('stopwords') # download stopwords\n",
        "nltk.download('wordnet')   # download vocab for lemmatizer"
      ],
      "execution_count": 10,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "[nltk_data] Downloading package stopwords to /root/nltk_data...\n",
            "[nltk_data]   Package stopwords is already up-to-date!\n",
            "[nltk_data] Downloading package wordnet to /root/nltk_data...\n",
            "[nltk_data]   Package wordnet is already up-to-date!\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "True"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 10
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "4AnMuLI0lDfL"
      },
      "source": [
        "import re\n",
        "from nltk.stem import WordNetLemmatizer \n",
        "from nltk.corpus import stopwords"
      ],
      "execution_count": 11,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "igbp2yH2q30j",
        "outputId": "6994abb9-4cd8-4842-b94a-d5db4efff5d1",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "stopwords_eng = set(stopwords.words('english'))\n",
        "len(stopwords_eng)"
      ],
      "execution_count": 12,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "179"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 12
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Nxl-zOnQg2XM"
      },
      "source": [
        "lemmatizer = WordNetLemmatizer()\n",
        "\n",
        "def clean_txt(txt):\n",
        "    txt = re.sub(r'([^\\s\\w])+', ' ', txt)\n",
        "    txt = \" \".join([lemmatizer.lemmatize(word) for word in txt.split()\n",
        "                    if not word in stopwords_eng])\n",
        "    txt = txt.lower()\n",
        "    return txt"
      ],
      "execution_count": 13,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "OxCUSWKMhLv0",
        "outputId": "0f982aa3-ba96-4432-9a20-1af5cd6b212c",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 121
        }
      },
      "source": [
        "X_train = df_train['x'].apply(lambda x: clean_txt(x))\n",
        "X_train[:5]"
      ],
      "execution_count": 14,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "0    ahhhh woken bad dream u tho dont like u right ...\n",
              "1                                        never nothing\n",
              "2    u sound like manky scouse boy steve like trave...\n",
              "3    mum say wan go go shun bian watch da glass exh...\n",
              "4    never lei v lazy got wat dat day ü send da url...\n",
              "Name: x, dtype: object"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 14
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "SokdTuEnsWCz"
      },
      "source": [
        "## Vectorize"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "gaww0SO3vrJh"
      },
      "source": [
        "from tensorflow.keras.preprocessing.text import Tokenizer\n",
        "from keras.preprocessing import sequence"
      ],
      "execution_count": 15,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "TsWMitwY97ie"
      },
      "source": [
        "# Keep top 1000 frequently occurring words\n",
        "max_words = 1000\n",
        "\n",
        "# Cut off the words after seeing 500 words in each document\n",
        "max_len = 500"
      ],
      "execution_count": 16,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "P4A3euifsX3t"
      },
      "source": [
        "t = Tokenizer(num_words=max_words)\n",
        "t.fit_on_texts(X_train)"
      ],
      "execution_count": 17,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "1f5dEVEn7hD_",
        "outputId": "5cb4d8d8-b4ce-4830-f2b1-fc0522ecc1b4",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 104
        }
      },
      "source": [
        "# Transform each text to a sequence of integers\n",
        "sequences = t.texts_to_sequences(X_train)\n",
        "sequences[:5]"
      ],
      "execution_count": 18,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "[[309, 227, 1, 587, 42, 15, 1, 90, 359, 13, 103, 54, 228, 86],\n",
              " [195, 252],\n",
              " [1, 310, 15, 219, 15, 43, 311, 37, 386, 1, 6, 338, 422],\n",
              " [477, 58, 188, 8, 8, 243, 43],\n",
              " [195, 478, 167, 821, 18, 77, 212, 12, 28, 22, 43, 124, 70, 24]]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 18
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "HMh3sBEb8Izt",
        "outputId": "db850928-ae1a-4ee6-9237-e03ac730dd7e",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 104
        }
      },
      "source": [
        "# Make all rows of equal length\n",
        "sequences_matrix = sequence.pad_sequences(sequences, maxlen=max_len)\n",
        "sequences_matrix[:5]"
      ],
      "execution_count": 19,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "array([[  0,   0,   0, ...,  54, 228,  86],\n",
              "       [  0,   0,   0, ...,   0, 195, 252],\n",
              "       [  0,   0,   0, ...,   6, 338, 422],\n",
              "       [  0,   0,   0, ...,   8, 243,  43],\n",
              "       [  0,   0,   0, ..., 124,  70,  24]], dtype=int32)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 19
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "tRXVlCIc82HB"
      },
      "source": [
        "## Build model"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "28FEAlrK84fo",
        "outputId": "320c415b-de2f-4849-bc6f-944748a550ce",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 364
        }
      },
      "source": [
        "i = tf.keras.layers.Input(shape=[max_len])\n",
        "x = tf.keras.layers.Embedding(max_words, 50, input_length=max_len)(i)\n",
        "x = tf.keras.layers.LSTM(64)(x)\n",
        "\n",
        "x = tf.keras.layers.Dense(256, activation='relu')(x)\n",
        "x = tf.keras.layers.Dropout(0.5)(x)\n",
        "x = tf.keras.layers.Dense(1, activation='relu')(x)\n",
        "\n",
        "model = tf.keras.models.Model(inputs=i, outputs=x)\n",
        "model.compile(\n",
        "    loss='binary_crossentropy',\n",
        "    optimizer='RMSprop',\n",
        "    metrics=['accuracy']\n",
        ")\n",
        "model.summary()"
      ],
      "execution_count": 20,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Model: \"functional_1\"\n",
            "_________________________________________________________________\n",
            "Layer (type)                 Output Shape              Param #   \n",
            "=================================================================\n",
            "input_1 (InputLayer)         [(None, 500)]             0         \n",
            "_________________________________________________________________\n",
            "embedding (Embedding)        (None, 500, 50)           50000     \n",
            "_________________________________________________________________\n",
            "lstm (LSTM)                  (None, 64)                29440     \n",
            "_________________________________________________________________\n",
            "dense (Dense)                (None, 256)               16640     \n",
            "_________________________________________________________________\n",
            "dropout (Dropout)            (None, 256)               0         \n",
            "_________________________________________________________________\n",
            "dense_1 (Dense)              (None, 1)                 257       \n",
            "=================================================================\n",
            "Total params: 96,337\n",
            "Trainable params: 96,337\n",
            "Non-trainable params: 0\n",
            "_________________________________________________________________\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Q99MXDnNBfku",
        "outputId": "2577ab19-5023-44ce-b05a-59ac476dbeb2",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 176
        }
      },
      "source": [
        "r = model.fit(sequences_matrix, y_train,\n",
        "              batch_size=128, epochs=10,\n",
        "              validation_split=0.2,\n",
        "              callbacks=[tf.keras.callbacks.EarlyStopping(\n",
        "                  monitor='val_loss', min_delta=0.0001)])"
      ],
      "execution_count": 21,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Epoch 1/10\n",
            "27/27 [==============================] - 20s 753ms/step - loss: 0.3418 - accuracy: 0.8771 - val_loss: 0.1466 - val_accuracy: 0.9522\n",
            "Epoch 2/10\n",
            "27/27 [==============================] - 19s 697ms/step - loss: 0.0979 - accuracy: 0.9806 - val_loss: 0.1138 - val_accuracy: 0.9868\n",
            "Epoch 3/10\n",
            "27/27 [==============================] - 18s 651ms/step - loss: 0.0687 - accuracy: 0.9889 - val_loss: 0.1134 - val_accuracy: 0.9880\n",
            "Epoch 4/10\n",
            "27/27 [==============================] - 18s 662ms/step - loss: 0.0644 - accuracy: 0.9910 - val_loss: 0.1186 - val_accuracy: 0.9904\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "JGsLmFZCZ8uv"
      },
      "source": [
        "## Evaluate"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "t4pd4gnPZkBi",
        "outputId": "d68a6515-3ad0-4d5a-e43b-8244d9d087fe",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 282
        }
      },
      "source": [
        "plt.plot(r.history['loss'], label='loss')\n",
        "plt.plot(r.history['val_loss'], label='val_loss')\n",
        "plt.legend()"
      ],
      "execution_count": 22,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "<matplotlib.legend.Legend at 0x7f3b2b80d5f8>"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 22
        },
        {
          "output_type": "display_data",
          "data": {
            "image/png": "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\n",
            "text/plain": [
              "<Figure size 432x288 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": [],
            "needs_background": "light"
          }
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "LmPihX-lZv2V",
        "outputId": "80f6b8ac-f597-4481-ad21-69810167fc14",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 282
        }
      },
      "source": [
        "plt.plot(r.history['accuracy'], label='acc')\n",
        "plt.plot(r.history['val_accuracy'], label='val_acc')\n",
        "plt.legend()"
      ],
      "execution_count": 23,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "<matplotlib.legend.Legend at 0x7f3b2c7c9550>"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 23
        },
        {
          "output_type": "display_data",
          "data": {
            "image/png": "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\n",
            "text/plain": [
              "<Figure size 432x288 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": [],
            "needs_background": "light"
          }
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "mfkccGB1apwU"
      },
      "source": [
        "def preprocessing(X):\n",
        "  x = X.apply(lambda x: clean_txt(x))\n",
        "  x = t.texts_to_sequences(x)\n",
        "  return sequence.pad_sequences(x, maxlen=max_len)"
      ],
      "execution_count": 24,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "fpwMTxKqaBkB",
        "outputId": "08a89a21-2d93-4b6a-a6ce-32082000e037",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 54
        }
      },
      "source": [
        "s = model.evaluate(preprocessing(df_test['x']), y_test)"
      ],
      "execution_count": 25,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "44/44 [==============================] - 3s 65ms/step - loss: 0.0956 - accuracy: 0.9842\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "_13xVHlCbU1o",
        "outputId": "d12fe29a-bacd-4c71-d100-b5f325343783",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "print('Loss: {:.3f}, Accuracy: {:.3f}'.format(s[0], s[1]))"
      ],
      "execution_count": 26,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Loss: 0.096, Accuracy: 0.984\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "YE1Ro3s2d9MQ"
      },
      "source": [
        "## Challenge"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "J9tD9yACG6M9",
        "outputId": "9e708134-c82c-4351-b7e8-68d899439ff5",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "# function to predict messages based on model\n",
        "# (should return list containing prediction and label, ex. [0.008318834938108921, 'ham'])\n",
        "def predict_message(pred_text):\n",
        "  p = model.predict(preprocessing(pd.Series([pred_text])))[0]\n",
        "\n",
        "  return (p[0], (\"ham\" if p<0.5 else \"spam\"))\n",
        "\n",
        "pred_text = \"how are you doing today?\"\n",
        "\n",
        "prediction = predict_message(pred_text)\n",
        "print(prediction)"
      ],
      "execution_count": 30,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "(0.0, 'ham')\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Dxotov85SjsC",
        "outputId": "3f2219df-9e51-4a37-e771-881878a0e0d2",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "# Run this cell to test your function and model. Do not modify contents.\n",
        "def test_predictions():\n",
        "  test_messages = [\"how are you doing today\",\n",
        "                   \"sale today! to stop texts call 98912460324\",\n",
        "                   \"i dont want to go. can we try it a different day? available sat\",\n",
        "                   \"our new mobile video service is live. just install on your phone to start watching.\",\n",
        "                   \"you have won £1000 cash! call to claim your prize.\",\n",
        "                   \"i'll bring it tomorrow. don't forget the milk.\",\n",
        "                   \"wow, is your arm alright. that happened to me one time too\"\n",
        "                  ]\n",
        "\n",
        "  test_answers = [\"ham\", \"spam\", \"ham\", \"spam\", \"spam\", \"ham\", \"ham\"]\n",
        "  passed = True\n",
        "\n",
        "  for msg, ans in zip(test_messages, test_answers):\n",
        "    prediction = predict_message(msg)\n",
        "    if prediction[1] != ans:\n",
        "      passed = False\n",
        "\n",
        "  if passed:\n",
        "    print(\"You passed the challenge. Great job!\")\n",
        "  else:\n",
        "    print(\"You haven't passed yet. Keep trying.\")\n",
        "\n",
        "test_predictions()\n"
      ],
      "execution_count": 31,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "You passed the challenge. Great job!\n"
          ],
          "name": "stdout"
        }
      ]
    }
  ]
}