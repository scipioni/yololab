#!/bin/bash

# https://github.com/AastaNV/JEP/blob/master/script/install_opencv4.6.0_Jetson.sh

RELEASE=4.8.0
PYTHON=python
BUILD=./build
CUDA_TOOLKIT_ROOT_DIR=/opt/cuda-11.7

#sudo apt install -y libdc1394-utils libdc1394-22-dev
#sudo apt remove -y libopencv libopencv-dev libopencv-python libopencv-samples

# xavier CUDA_ARCH_BIN=7.2
#CUDA="-D CUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda -D WITH_CUDA=ON -D WITH_CUDNN=ON -D CUDA_GENERATION=Auto"


mkdir -p $BUILD
cd $BUILD

if [ ! -d opencv-$RELEASE ]; then
	[ -f opencv-$RELEASE.tar.gz ] || curl -L https://github.com/opencv/opencv/archive/${RELEASE}.tar.gz -o opencv-${RELEASE}.tar.gz
	tar xf opencv-$RELEASE.tar.gz
fi

if [ ! -d opencv_contrib-$RELEASE ]; then
	curl -L https://github.com/opencv/opencv_contrib/archive/${RELEASE}.tar.gz -o opencv_contrib-${RELEASE}.tar.gz
	tar xf opencv_contrib-${RELEASE}.tar.gz
fi


cd opencv-$RELEASE

rm -fR release
mkdir -p release
cd release

JOBS=$(getconf _NPROCESSORS_ONLN)
JOBS=$(($JOBS - 1)) 

export CC=gcc-12
export CXX=g++-12

cmake \
	-D BUILD_LIST=core,improc,videoio,dnn,python3,cudev,dnn_objdetect,highgui,video,calib3d,gapi \
	-D WITH_CUDA=ON \
	-D WITH_CUDNN=ON \
	-D CUDA_ARCH_BIN="7.2,8.7" \
	-D CUDA_ARCH_PTX="" \
	-D OPENCV_GENERATE_PKGCONFIG=ON \
	-D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-${RELEASE}/modules \
	-D WITH_GSTREAMER=ON \
	-D WITH_LIBV4L=ON \
	-D PYTHON_EXECUTABLE=$(which $PYTHON) \
	-D OPENCV_PYTHON3_INSTALL_PATH=$($PYTHON -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
	-D BUILD_opencv_python3=ON \
	-D BUILD_opencv_python2=OFF \
	-D BUILD_TESTS=OFF \
	-D BUILD_PERF_TESTS=OFF \
	-D BUILD_EXAMPLES=OFF \
	-D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=$($PYTHON -c "import sys; print(sys.prefix)") \
	-D CUDA_TOOLKIT_ROOT_DIR=${CUDA_TOOLKIT_ROOT_DIR} \
	..

make -j${JOBS} install/strip

