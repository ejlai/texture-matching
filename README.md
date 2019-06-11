# Texture Matching using Local Binary Patterns (LBP)

## Updated for Python 3.x (Tested on Python 3.6.7, ubutnu 18.04)

__8-bit binary array value calculation__

If the neighbouring pixel value is greater or equal to the central pixel value, the corresponding bit in the binary array is set to 1 else the corresponding bit in the binary array is set to 0. 
(LBP at wiki page, https://en.wikipedia.org/wiki/Local_binary_patterns)

Related blog post explaining the code - [Click
Here](http://hanzratech.in/2015/05/30/local-binary-patterns.html)

## Install packages for Python3

```
$ pip3 install joblib
$ pip3 install cvutils
...

```

## Usage

__Clone the Project__

From ubuntu terminal
```
$ git clone https://github.com/ejlai/texture-matching.git
$ cd texture-matching

```

__Perform training using__

```
texture-matching$ sudo python3 perform-training.py -t data/lbp/train/ -l data/lbp/class_train.txt

```

__Perform testing using__

```
python perform-testing.py -t data/lbp/test/ -l data/lbp/class_test.txt
```
## Results

Let's check out the results.

__Input Image -- ROCK Class__

Here is an input image of a rock texture.

![alt tag](docs/images/query-image-1.png)

_Matching Scores_ - Below are the sorted results of matching. The top 2 scores are of rock texture.

![alt tag](docs/images/query-image-results-1.png)

__Input Image -- CHECKERED Class__

Here is an input image of a checkered texture .

![alt tag](docs/images/query-image-2.png)

_Matching Scores_ - Below are the sorted results of matching. The top 2 scores are of checkered texture.

![alt tag](docs/images/query-image-results-2.png)

__Input Image -- GRASS Class__

Here is an input image of a grass texture.

![alt tag](docs/images/query-image-3.png)

_Matching Scores_ - Below are the sorted results of matching. The top 2 scores are of grass texture.

![alt tag](docs/images/query-image-results-3.png)
