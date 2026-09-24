# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_lab111_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED lab111_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(lab111_FOUND FALSE)
  elseif(NOT lab111_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(lab111_FOUND FALSE)
  endif()
  return()
endif()
set(_lab111_CONFIG_INCLUDED TRUE)

# output package information
if(NOT lab111_FIND_QUIETLY)
  message(STATUS "Found lab111: 0.0.0 (${lab111_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'lab111' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${lab111_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(lab111_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${lab111_DIR}/${_extra}")
endforeach()
