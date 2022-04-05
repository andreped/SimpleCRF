cmake_minimum_required (VERSION 2.6)
project(densecrf)

if(APPLE)
	set(CMAKE_OSX_DEPLOYMENT_TARGET "10.13" CACHE STRING "Minimum OS X deployment version")
endif()

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PROJECT_SOURCE_DIR}/cmake)

include_directories( include )

add_subdirectory (src)
add_subdirectory (examples)
add_subdirectory (external)
