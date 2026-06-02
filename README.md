The following is a set of instructions for a Tensorflow Object Detection and Image Classification program. This mostly assumes you are using Unix (Windows just means you will have to use different command syntax). Code in bold indicates it will be variable to your personal computer, and the words are metaphorical instructions for what you actually need. 

# Tensorflow Object Detection
## CONFIGURING YOUR ENVIRONMENT
### 1. Creating a virtual environment
Firstly, you will want to create a conda virtual environment to contain all your specific packages and their versions, to prevent crossover into your other projects. Download and install conda whenever and however; there are plenty of tutorials. 

Then, paste this into terminal:
> conda create -n tensorflow pip python=3.10.18

This creates the VE. You may activate with each session via:
> conda activate tensorflow

### 2. Installing Tensorflow
Inside this environment, you will want to download Tensorflow itself. This can be done via the following command:
> pip install --ignore-installed --upgrade tensorflow==2.13.1

You may verify this worked via:
> python -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))"

### 3. Download TF Object Detection API
These folders and files basically provide you an accessible human interface for leveraging Tensorflow’s programs, with pre-built code and all. 
Firstly, you will want to create a new folder named _Tensorflow_. __cd__ into this directory. Download the [Tensorflow Model Repository](https://github.com/tensorflow/models/archive/master.zip) as a ZIP, and extract its contents here. You can alternatively clone it via Github if you’re a nerd. 

### 4. Protobuf Installation/Complication
This package helps Tensorflow Object Detection API configure model/training parameters. Whatever that means, it’s important enough to make you deal with compiling it. 
Basically, go [here](https://github.com/protocolbuffers/protobuf/releases/tag/v23.2) and download whichever ZIP/tar matches your OS.
Then, extract the contents of the ZIP/tar in whatever directory you want. Again, you can clone Github alternatively.
Next, add the PATH to these extracted contents to your Path environment. How to do this based on your OS, but works like this in Unix tsch:
	a. Open your hidden configuration file: 
	    > nano ~/.tcshrc
	b. Paste this at the end of it: 
	    > set path = ( $path __/full/path/to/your/protoc/__ bin )
Once this is set, cd into _Tensorflow/models/research_ and then paste this:
> for /f %i in ('dir /b object_detection\protos\*.proto') do protoc object_detection\protos\%i --python_out=.

### 5. COCO API installation
Download [cocoapi](https://github.com/cocodataset/cocoapi) as ZIP to whatever directory you want and extract its contents (Github clone alternately). Then run the following:
> cd cocoapi/PythonAPI
> make
> cp -r pycocotools full/path/to/this/folder/TensorFlow/models/research/

### 6. Install Object Detection API
Go in _Tensorflow/models/research_ and paste this code:
> cp object_detection/packages/tf2/setup.py .
> python -m pip install .

### 7. Test Installation
To make sure Tensorflow and Object Detection API work and play nicely, see if it passes these tests. 
Within _Tensorflow/models/research_,
> python object_detection/builders/model_builder_tf2_test.py

It will tell you if something went wrong.

## TRAINING/RUNNING A DETECTION MODEL
Now that everything is installed properly, it is time to actually train a model.
### 1. Workspace Preparation
Create a new folder entitled _workspace_ under _Tensorflow_. Then, under _workspace_, create a folder _training_demo_. This will be where you train a particular model. Under _Tensorflow/workspace/training_demo/_, you should create the following other folders:
- /annotations/ : This will store the *.record files
- /exported-models/ : Finished model will be stored here, for export
- /images/: Set of images for training/testing, with *.xml files
- /models/ : Will contain subfolders of each model trained upon
- /pre-trained-models/ : Where the downloaded, pre-trained-models will be stored

### 2. Dataset Preparation
First, you will need to install __labelImg__ to annotate the dataset. Here’s the simplest way:
> pip install labelImg
> labelImg __/path/to/images__ [class file]

Then, comes annotation. In terminal,
> labelImg __/path/to/__ Tensorflow/workspace/training_demo/images

Information about how to further utilize labelImg can be found [here](https://github.com/HumanSignal/labelImg#usage). This will create xml files alongside your images to store annotation information. 

### 3. Dataset Partition
Once you have all your images annotated, you are going to want to split them into training and testing sets for the model. The standard ratio is 80:20 for training:testing; however, if your dataset is large enough, you may want to do 90:10 to maximize training data. 

While this may be done manually, pre-built code helps this go faster. 
Create the following directory: _Tensorflow/scripts/preprocessing_
And put this [file](https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/_downloads/d0e545609c5f7f49f39abc7b6a38cec3/partition_dataset.py) in it.
cd into _proprocessing_ and run:
> python partition_dataset.py -x -i __/path/to/__ Tensorflow/workspace/training_demo/images -r 0.2

This divides your image set into train and test, with an 80:20 split. This only copies the images into these directories; you’ll have to delete the originals.

### 4. Create Label Map
Tensorflow requires a file to map label names onto integer values. This should be in .pbtxt format (e.g. label.pbtxt), creatable via any text editor. The file should be in this format:

```
 item {
       id: 1		#integer value
       name: ‘class1’	#class label
 }
 
 item {
        id: 2		
        name: ‘class2’
 }
```

Stick this in the annotations folder.

### 5. Create Records
We need to convert all the xml files in images into a TFRecord format. There is [pre-built code](https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/_downloads/da4babe668a8afb093cc7776d7e630f3/generate_tfrecord.py) for this, to be saved in _scripts/preprocessing_. 
Firstly, install the package __pandas__ via conda or pip.
Then, go into _preprocessing_  and run:

> #Training TFRecord
> python generate_tfrecord.py -x path/to/Tensorflow/workspace/training_demo/images/train -l path/to/Tensorflow/workspace/training_demo/annotations/label_map.pbtxt -o path/to/Tensorflow/workspace/training_demo/train.record

> #Testing TFRecord
> python generate_tfrecord.py -x path/to/Tensorflow/workspace/training_demo/images/test -l path/to/Tensorflow/workspace/training_demo/annotations/label_map.pbtxt -o path/to/Tensorflow/workspace/training_demo/test.record

This will create train.record and test.record files in the _annotations_ folder. 

### 6. Get a pre-trained model
Now that the workspace is properly set-up and all necessary files exist, it is time to start the training. First, you will need to acquire some pre-trained model from [Tensorflow 2 Detection Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md). You can get the statistics of and information about each model to determine which one may work the best for your dataset. Once you downloaded the __*.tar.gz__ of the pre-trained model, open the __*.tar__ folder and extract its contents into _training_demo/pre-trained-models_. 

Now that you have the pre-trained model saved, copy this folder into models and name it after the pretrained model (e.g. copy _training_demo/pre-trained-models/ssd_resnet50_v1_fpn_640x640_coco17_tpu-8_ into models, rename it _my_ssd_resnet50_v1_fpn_.)

In this new folder in models, make a few changes to its pipeline.config. Note this will look different for each pre-trained model; these are just the basic changes:

```
  1 model {
  2  ssd {
  3    __num_classes: 1 # Set this to the number of different label classes__
  4    image_resizer {
  5      fixed_shape_resizer {
  6        height: 640
  7        width: 640
  8      }
  9    }
 10    feature_extractor {
 11      type: "ssd_resnet50_v1_fpn_keras"
 12      depth_multiplier: 1.0
 13      min_depth: 16
 14      conv_hyperparams {
 15        regularizer {
 16          l2_regularizer {
 17            weight: 0.00039999998989515007
 18          }
 19        }
 20        initializer {
 21          truncated_normal_initializer {
 22            mean: 0.0
 23            stddev: 0.029999999329447746
 24          }
 25        }
 26        activation: RELU_6
 27        batch_norm {
 28          decay: 0.996999979019165
 29          scale: true
 30          epsilon: 0.0010000000474974513
 31        }
 32      }
 33      override_base_feature_extractor_hyperparams: true
 34      fpn {
 35        min_level: 3
 36        max_level: 7
 37      }
 38    }
 39    box_coder {
 40      faster_rcnn_box_coder {
 41        y_scale: 10.0
 42        x_scale: 10.0
 43        height_scale: 5.0
 44        width_scale: 5.0
 45      }
 46    }
 47    matcher {
 48      argmax_matcher {
 49        matched_threshold: 0.5
 50        unmatched_threshold: 0.5
 51        ignore_thresholds: false
 52        negatives_lower_than_unmatched: true
 53        force_match_for_each_row: true
 54        use_matmul_gather: true
 55      }
 56    }
 57    similarity_calculator {
 58      iou_similarity {
 59      }
 60    }
 61    box_predictor {
 62      weight_shared_convolutional_box_predictor {
 63        conv_hyperparams {
 64          regularizer {
 65            l2_regularizer {
 66              weight: 0.00039999998989515007
 67            }
 68          }
 69          initializer {
 70            random_normal_initializer {
 71              mean: 0.0
 72              stddev: 0.009999999776482582
 73            }
 74          }
 75          activation: RELU_6
 76          batch_norm {
 77            decay: 0.996999979019165
 78            scale: true
 79            epsilon: 0.0010000000474974513
 80          }
 81        }
 82        depth: 256
 83        num_layers_before_predictor: 4
 84        kernel_size: 3
 85        class_prediction_bias_init: -4.599999904632568
 86      }
 87    }
 88    anchor_generator {
 89      multiscale_anchor_generator {
 90        min_level: 3
 91        max_level: 7
 92        anchor_scale: 4.0
 93        aspect_ratios: 1.0
 94        aspect_ratios: 2.0
 95        aspect_ratios: 0.5
 96        scales_per_octave: 2
 97      }
 98    }
 99    post_processing {
100      batch_non_max_suppression {
101        score_threshold: 9.99999993922529e-09
102        iou_threshold: 0.6000000238418579
103        max_detections_per_class: 100
104        max_total_detections: 100
105        use_static_shapes: false
106      }
107      score_converter: SIGMOID
108    }
109    normalize_loss_by_num_matches: true
110    loss {
111      localization_loss {
112        weighted_smooth_l1 {
113        }
114      }
115      classification_loss {
116        weighted_sigmoid_focal {
117          gamma: 2.0
118          alpha: 0.25
119        }
120      }
121      classification_weight: 1.0
122      localization_weight: 1.0
123    }
124    encode_background_as_zeros: true
125    normalize_loc_loss_by_codesize: true
126    inplace_batchnorm_update: true
127    freeze_batchnorm: false
128  }
129}
130train_config {
131  batch_size: 8 # Increase/Decrease this value depending on the available memory (Higher values require more memory and vice-versa)
132  data_augmentation_options {
133    random_horizontal_flip {
134    }
135  }
136  data_augmentation_options {
137    random_crop_image {
138      min_object_covered: 0.0
139      min_aspect_ratio: 0.75
140      max_aspect_ratio: 3.0
141      min_area: 0.75
142      max_area: 1.0
143      overlap_thresh: 0.0
144    }
145  }
146  sync_replicas: true
147  optimizer {
148    momentum_optimizer {
149      learning_rate {
150        cosine_decay_learning_rate {
151          learning_rate_base: 0.03999999910593033
152          total_steps: 25000
153          warmup_learning_rate: 0.013333000242710114
154          warmup_steps: 2000
155        }
156      }
157      momentum_optimizer_value: 0.8999999761581421
158    }
159    use_moving_average: false
160  }
161  fine_tune_checkpoint: "pre-trained-models/your_pretrained_model/checkpoint/ckpt-0" # Path to checkpoint of pre-trained model
162  num_steps: 25000
163  startup_delay_steps: 0.0
164  replicas_to_aggregate: 8
165  max_number_of_boxes: 100
166  unpad_groundtruth_tensors: false
167  fine_tune_checkpoint_type: "detection" # Set this to "detection" since we want to be training the full detection model
168  use_bfloat16: false # Set this to false if you are not training on a TPU
169  fine_tune_checkpoint_version: V2
170}
171train_input_reader {
172  label_map_path: "path/to/Tensorflow/workspace/training_demo/annotations/label_map.pbtxt" # Path to label map file
173  tf_record_input_reader {
174    input_path: "path/to/Tensorflow/workspace/training_demo/annotations/train.record" # Path to training TFRecord file
175  }
176}
177 eval_config {
178  metrics_set: "coco_detection_metrics"
179  use_moving_averages: false
180}
181 eval_input_reader {
182  label_map_path: "path/to/Tensorflow/workspace/training_demo/annotations/label_map.pbtxt" # Path to label map file
183  shuffle: false
184  num_epochs: 1
185  tf_record_input_reader {
186    input_path: "path/to/Tensorflow/workspace/training_demo/annotations/test.record" # Path to testing TFRecord
187  }
188}
```

### 7. Train the Model
From _Tensorflow/models/research/object_detection/model_main_tf2.py_, copy the model_main_tf2.py script into training_demo.
Then run the following:
> python model_main_tf2.py --model_dir=models/your_model_folder --pipeline_config_path=models/your_model_folder/pipeline.config

This initiates model training. It can take a day or up to a week; it’s strongly recommended you do not try to run this on a local computer, but rather look for an HPC system you can use. 

### 8. Evaluate the Model
You’ll want to check how the model training is doing. Inside training_demo, run the following command:
> python model_main_tf2.py --model_dir=models/your_model_folder --pipeline_config_path=models/your_model_folder/pipeline.config --checkpoint_dir=models/your_model_folder

This will spit out evaluation metrics based on the most recent checkpoint.

### 9. Export the Model
Once the model is trained to your liking, you’ll want to prep it for export. Copy the _TensorFlow/models/research/object_detection/exporter_main_v2.py_ script into the training_demo folder. Then, run the following command in training_demo:

> python exporter_main_v2.py --input_type image_tensor --pipeline_config_path models/your_model_folder/pipeline.config --trained_checkpoint_dir models/your_model_folder/ --output_directory exported-models/my_model

This saved model, under my_model, can then be used for interference. 

### 10. Using the Model for Interference
In the GitHub repository, I’ve saved a Jupyter notebook entitled Run_and_Crop.ipynb under testspace. This can be followed and adapted for your specific purposes based on the comments. Here are come quick things to configure your environment:
- Under _Tensorflow/testspace/images_, you can insert a local set of images you want to run object detection on
- You need to move your exported model folder (my_model) and a copy of label_map.pbtxt into testspace to perform interference
- My code saves images of the individual detected objects, not a copy of the image with detections
- Code that is highlighted out is optional. Some of it is just annoying on a large-scale detection operation; e.g showing each cropped image


# Tensorflow Image Classification
In the GitHub repository, I’ve saved a Jupyter notebook entitled Image_Classification.ipynb under testspace. Here are some basic instructions; the code itself will take you most of the way.
### 1. Configure Your Environment
For my image classification code, I have it set as Tensorflow version 2.15.0. This is different from the Object Detection; you will need a separate virtual environment. 

### 2. Dataset Preparation
Under _testspace/classification_images_, create folders entitled under each sorting category you want. e.g, _testspace/classification_images/class_1_, _testspace/classification_images/class_2_. You will fill these folders with training images relevant to each category. 

The code will take you through splitting the dataset into training/validation and normalizing it.

### 3. Training the Model
While the code takes you through training and saving the model, note that there are several other pre-trained-models you made find under Tensorflow, and it also has tutorials on building a model from scratch. My specific model may not be best for your data. 

### 4. Evaluating the Model
A classification matrix is utilized to help you visualize the results of your model, You are looking for a solid dark blue diagonal. 

The rest of the code has to do with deploying the image classification model; create directories as needed for showing your output.     
