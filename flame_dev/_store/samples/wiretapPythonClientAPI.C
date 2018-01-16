//*****************************************************************************/
// This file contains the source code to create Python bindings for the
// Wiretap client API.  Users are free to copy or use this code at will.
//
//*****************************************************************************/

// Boost Includes ==============================================================
#include <boost/python.hpp>
#include <boost/cstdint.hpp>
#include <boost/python/detail/api_placeholder.hpp>

// Includes ====================================================================
#include <WireTapClientAPI.h>
#include <WireTapTypes.h>

// Using =======================================================================
using namespace boost::python;

// Declarations ================================================================

// A WireTapInt class is used as a wrapper class for an integer. This
// is needed due to the fact that python's int is not mutable. All functions
// in WireTap Client API returns boolean status value. Therefore, for those
// functions that want their referenced int parameter(s) to reflect the resulting
// value after the function is called, instead of using int& in the parameter,
// WireTapInt& should be used. (Note: In Python, only objects are mutable.
// The basic types, such as int, double, etc. are not mutable).
class WireTapInt
{
public:
    int integerValue;

    WireTapInt( int intValue  = 0 ):
      integerValue(intValue) {}

    WireTapInt& operator=( const WireTapInt& newInt )
    { 
      if (this != &newInt)
      {
        integerValue = ( int )newInt;
      }
      return *this;
    }

    WireTapInt& operator=( const int& newInt)
    {
      integerValue = newInt;
      return *this;
    }

    bool operator<( const int& anotherInt )
    {
      if( integerValue < anotherInt )
      {
        return true;
      }

      return false;
    }

    bool operator>( const int& anotherInt )
    {
      if( integerValue > anotherInt )
      {
        return true;
      }

      return false;
    }

    bool operator==( const int& anotherInt )
    {
      if( integerValue == anotherInt )
      {
        return true;
      }

      return false;
    }

    bool operator==( const WireTapInt& anotherWireTapInt )
    {
      if( integerValue == ( int )anotherWireTapInt )
      {
        return true;
      }

      return false;
    }

    operator int() const
    {
      return integerValue; 
    }
};

// Anonymous namespace
//
#if defined(__GNUC__) && (__GNUC__ * 1000 + __GNUC_MINOR) <= 4001 && defined(PYTHON_DWA2002810_HPP)
#define SKIP_ANON_NAMESPACE
#endif
#ifndef SKIP_ANON_NAMESPACE
namespace  {
#endif

  // This is a WireTapMetatData::Blob  wrapper class that derives from 
  // WireTapMetaData::Blob. This wrapper class is needed because python's 
  // int is immutable. Therefore, when trying to call the API method from 
  // python, instead of passing int& as parameter, we need to pass the 
  // WireTapInt& instead.
  struct Blob_Wrapper : WireTapMetaData::Blob
  {
    Blob_Wrapper( const char *originalData, const char *format, int versionMajor, int versionMinor ):
      WireTapMetaData::Blob( originalData, format, versionMajor, versionMinor ) {}
                                                                                                             
    Blob_Wrapper( const char *rawData ):
      WireTapMetaData::Blob(rawData) {}

    bool getVersionWrapperFunction( WireTapInt &major, WireTapInt &minor ) const
    {
      return WireTapMetaData::Blob::getVersion( major.integerValue, 
                                                minor.integerValue );
    }
  };

  // This is a WireTapServerList wrapper class that derives from WireTapServerList.
  // This wrapper class is needed because python's int is immutable. Therefore, when
  // trying to call the API method from python, instead of passing int& as parameter,
  // we need to pass the WireTapInt& instead.
  struct WireTapServerList_Wrapper: WireTapServerList
  {
    WireTapServerList_Wrapper():
      WireTapServerList() {}   
 
    WireTapServerList_Wrapper(const char* database, const char* gatewayIpAddr):
      WireTapServerList( database, gatewayIpAddr ) {}

    bool getNumNodesWrapperFunction( WireTapInt &numberOfNodes )
    {
      return getNumNodes( numberOfNodes.integerValue );
    }
  };

  // This is a WireTapNodeHandle wrapper class that derives from WireTapNodeHandle.
  // It is needed because:
  // 1. There are 2 virtual functions (getMetaData/setMetaData).
  // 2. The readFrame/writeFrame functions are using a void* buffer argument which  
  //    cannot be exposed to python.  So the solution is to expose 2 functions
  //    wrapping them but receiving a char* pointer from python instead of a void*
  //    pointer.
  // 3. The function "linkToFrames()" is expecting an array of WireTapstr from
  //    python. However, python can only create a 'list' of WireTapStr, because
  //    array in python is reserved only for basic types such as int, char.
  //    Therefore, a wrapper to convert a list of WireTapStr in python to
  //    an array of WireTapStr is needed.
  // 4. The functions 
  //       getNumChildren, getNumFrames, getNodeType, getNumAvailableMetaDataStreams
  //    expect int& as parameters. However, Python's int is immutable, which means 
  //    when calling these funtions within python, passing int& is not allowed. Hence, 
  //    wrapper functions are needed so that for these 4 functions, we pass 
  //    WireTapInt& as parameters (instead of int&) within Python scripts/programs.
  // 5. The function
  //       getIsClipNode expects bool& as a parameter, so we pass a WireTapInt, which
  //       is mutable
  struct WireTapNodeHandle_Wrapper: WireTapNodeHandle
  {
    WireTapNodeHandle_Wrapper(PyObject* py_self_):
      WireTapNodeHandle(), py_self(py_self_) {}

    WireTapNodeHandle_Wrapper(PyObject* py_self_, const WireTapNodeHandle& node):
      WireTapNodeHandle(node), py_self(py_self_) {}

    WireTapNodeHandle_Wrapper(PyObject* py_self_, const WireTapServerHandle& server, const WireTapNodeId& nodeId):
      WireTapNodeHandle(server, nodeId), py_self(py_self_) {}

    WireTapNodeHandle_Wrapper(PyObject* py_self_, const WireTapServerHandle& server, const char* nodeIdStr):
      WireTapNodeHandle(server, nodeIdStr), py_self(py_self_) {}

    bool getMetaData(const char* streamName, const char* filter, const int depth, WireTapStr& metaData) const
    {
      return call_method< bool >(py_self, "getMetaData", streamName, filter, depth, metaData);
    }

    bool default_getMetaData(const char* streamName, const char* filter, const int depth, WireTapStr& metaData) const 
    {
      return WireTapNodeHandle::getMetaData(streamName, filter, depth, metaData);
    }

    bool readFrameWrapperFunction(int frameIndex, char * params, int paramsSize, char* buf, int bufSize)
    {
      return WireTapNodeHandle::readFrame(frameIndex, (void*)params, paramsSize, (void*)buf, bufSize);
    }

    bool readFrameWrapperFunction(int frameIndex, char* buf, int bufSize)
    {
      return readFrameWrapperFunction( frameIndex, 0 /* params*/, 0 /* paramsSize */, buf, bufSize );
    }

    bool writeFrameWrapperFunction(int frameIndex, const char* buf, int bufSize)
    {
      return WireTapNodeHandle::writeFrame(frameIndex, (void*)buf, bufSize);
    }

    bool linkToFramesWrapperFunction( boost::python::list pathList)
    {
      const int numPaths = boost::python::len( pathList );
      WireTapStr * paths = new WireTapStr[ numPaths ];
      for( int i = 0; i < numPaths; i++ )
      {
        paths[i] = boost::python::extract<WireTapStr>( pathList[i] );
      }
      
      const bool retVal = WireTapNodeHandle::linkToFrames( paths, numPaths );

      delete [] paths;
      
      return retVal;
    }

    bool getNumChildrenWrapperFunction( WireTapInt &numChildren ) const
    {
      unsigned value = 0;
      const bool ret = WireTapNodeHandle::getNumChildren( value );
      if ( ret ) { numChildren.integerValue = value; }
      return ret;
    }

    bool getNumFramesWrapperFunction( WireTapInt &numFrames ) const
    {
      unsigned value = 0;
      const bool ret = WireTapNodeHandle::getNumFrames( value );
      if ( ret ) { numFrames.integerValue = value; }
      return ret;
    }

    bool getNodeTypeWrapperFunction( WireTapInt &type ) const
    {
      return WireTapNodeHandle::getNodeType( type.integerValue );
    }

    bool getNumAvailableMetaDataStreamsWrapperFunction( WireTapInt &numStreams ) const
    {
      return WireTapNodeHandle::getNumAvailableMetaDataStreams( numStreams.integerValue );
    }

    bool getIsClipNodeWrapperFunction( WireTapInt &isClip ) const
    {
      bool b, ret; 
      ret = WireTapNodeHandle::getIsClipNode( b );
      isClip.integerValue = b;
      return ret;
    }

    PyObject* py_self;
  };

  // This is a WireTapServerHandle wrapper class that derives from WireTapServerHandle.
  // It is needed because:
  // 1. The readFrame/writeFrame/readStream functions are using a void* buffer 
  //    argument which cannot be exposed to python.  So the solution is to 
  //    expose 2 functions wrapping them but receiving a char* pointer from 
  //    python instead of a void* pointer.
  // 2. The functions getVersion/getProtocalVersion/readStream expect int& as 
  //    parameters. However, Python's int is immutable, which means when calling 
  //    these funtions within python, passing int& is not allowed. Hence, 
  //    wrapper functions are needed so that for these 4 functions, we pass 
  //    WireTapInt& as parameters (instead of int&) within Python 
  //    scripts/programs.
  // 3. The ping method has a parameter with a default value.  Default parameters
  //    are not supported when creating wrappers to expose methods.
  //    So here we create a "thin-wrapper" to be able to call ping without param.
  //
  struct WireTapServerHandle_Wrapper : WireTapServerHandle
  {
    WireTapServerHandle_Wrapper(PyObject* py_self_,const WireTapServerId & id):
      WireTapServerHandle(id), py_self(py_self_) {}

    WireTapServerHandle_Wrapper(PyObject* py_self_, const char *hostname = "localhost"):
      WireTapServerHandle(hostname), py_self(py_self_) {}

    WireTapServerHandle_Wrapper(PyObject* py_self_, const WireTapServerHandle &server):
      WireTapServerHandle(server), py_self(py_self_) {}

    bool readFrameWrapperFunction(const char *frameId, char* buf, int bufSize) 
    {
      return WireTapServerHandle::readFrame(frameId, (void*)buf,bufSize);
    }

    bool writeFrameWrapperFunction(const char *frameId, const char* buf, int bufSize) 
    {
      return WireTapServerHandle::writeFrame(frameId, (void*)buf, bufSize);
    }
 
    bool getVersionWrapperFunction( WireTapInt &major, 
                                    WireTapInt &minor ) const
    {
      return WireTapServerHandle::getVersion( major.integerValue, 
                                              minor.integerValue );
    }

    bool getProtocolVersionWrapperFunction( WireTapInt &major,
                                            WireTapInt &minor ) const
    {
      return WireTapServerHandle::getProtocolVersion( major.integerValue, 
                                                      minor.integerValue );
    }

    bool readStreamWrapperFunction(const char *streamId, char *buf, int bufSize,
                     int itemOffset, int itemSizeInBytes, WireTapInt &numItems )
    {
      return WireTapServerHandle::readStream(streamId, (void*)buf, bufSize,
                     itemOffset, itemSizeInBytes, numItems.integerValue );
    }

    // Thin wrapper to be able to call the version of ping with 0 parameter,
    // using the default value to timeoutMS parameter.
    // Default values are not supported when exposing methods with wrappers.
    bool ping() const
    {
      return WireTapServerHandle::ping();
    }


    PyObject* py_self;
  };
#ifndef SKIP_ANON_NAMESPACE
} // namespace
#endif

// Boost python wrapping code section
//
// define here the module "libwiretapPythonClientAPI", the name of this module
// should match the name of the .so/.dll file.
//
BOOST_PYTHON_MODULE(libwiretapPythonClientAPI)
{
  // Expose the WireTapStr class 
  class_< WireTapStr >("WireTapStr", init< optional< const char* > >())
    .def(init< const WireTapStr& >())
    .def("reset", &WireTapStr::reset)
    .def("length", &WireTapStr::length)
    .def("c_str", &WireTapStr::c_str)
    .def( self == self )
    .def("__str__", &WireTapStr::operator const char*)
  ;

  // Expose the WireTapStrList class 
  class_< WireTapStrList >("WireTapStrList", init<  >())
    .def("reserve", &WireTapStrList::reserve)
    .def("resize", &WireTapStrList::resize)
    .def("size", &WireTapStrList::size)
    .def("push_back", &WireTapStrList::push_back)
    .def( self == self )
    .def("getStr", &WireTapStrList::getStr)
  ;

  // Expose the public WireTapServerInfo class
  //
  class_< WireTapServerInfo >("WireTapServerInfo", init<  >())
    .def("getHostname",     &WireTapServerInfo::getHostname)
    .def("getDisplayName",  &WireTapServerInfo::getDisplayName)
    .def("getId",           &WireTapServerInfo::getId)
    .def("getVersionMajor", &WireTapServerInfo::getVersionMajor)
    .def("getVersionMinor", &WireTapServerInfo::getVersionMinor)
    .def("getVersionMaint", &WireTapServerInfo::getVersionMaint)
    .def("getProduct",      &WireTapServerInfo::getProduct)
    .def("getVendor",       &WireTapServerInfo::getVendor)
    .def("getProductVersionMajor", &WireTapServerInfo::getProductVersionMajor)
    .def("getProductVersionMinor", &WireTapServerInfo::getProductVersionMinor)
    .def("getProductVersionMaint", &WireTapServerInfo::getProductVersionMaint)
    .def("getProductBuild", 	   &WireTapServerInfo::getProductBuild)
    .def("getProductVersionStr",   &WireTapServerInfo::getProductVersionStr)
    .def("getStorageId",   	   &WireTapServerInfo::getStorageId)
  ;

  // Expose the WireTapOS class in the WireTapOS scope (WireTapOS_scope)
  //
  scope* WireTapOS_scope = new scope(
  class_< WireTapOS >("WireTapOS", init<  >())
    .def(init< const WireTapOS& >())
    .def("OS_TYPE_UNKNOWN_STR", &WireTapOS::OS_TYPE_UNKNOWN_STR)
    .def("OS_TYPE_IRIX_STR",    &WireTapOS::OS_TYPE_IRIX_STR)
    .def("OS_TYPE_LINUX_STR",   &WireTapOS::OS_TYPE_LINUX_STR)
    .def("OS_TYPE_WINNT_STR",   &WireTapOS::OS_TYPE_WINNT_STR)
    .def("OS_TYPE_MACOSX_STR",  &WireTapOS::OS_TYPE_MACOSX_STR)
    .def("getOSType",           &WireTapOS::getOSType)
    .def("getOSVersion",        &WireTapOS::getOSVersion)
    .def("getHostName",         &WireTapOS::getHostName)
    .def("strToOsType",         &WireTapOS::strToOsType)
    .def("OsTypeStr",           &WireTapOS::OsTypeStr)
    .staticmethod("getOSType")
    .staticmethod("getHostName")
    .staticmethod("OS_TYPE_WINNT_STR")
    .staticmethod("OsTypeStr")
    .staticmethod("OS_TYPE_MACOSX_STR")
    .staticmethod("OS_TYPE_UNKNOWN_STR")
    .staticmethod("OS_TYPE_IRIX_STR")
    .staticmethod("strToOsType")
    .staticmethod("getOSVersion")
    .staticmethod("OS_TYPE_LINUX_STR")
  );

  // Expose the WireTapOS::OsType Enum as WireTapOS.OsType
  //
  enum_< WireTapOS::OsType >("OsType")
    .value("OS_MACOSX",  WireTapOS::OS_MACOSX)
    .value("OS_WINNT",   WireTapOS::OS_WINNT)
    .value("OS_IRIX",    WireTapOS::OS_IRIX)
    .value("OS_LINUX",   WireTapOS::OS_LINUX)
    .value("OS_UNKNOWN", WireTapOS::OS_UNKNOWN)
  ;

  // Delete the scope
  //
  delete WireTapOS_scope;

  // Expose the WireTapFrameId class
  //
  class_< WireTapFrameId >("WireTapFrameId", init< optional< const char* > >())
    .def(init< const WireTapStr& >())       // Parameter constructor
    .def(init< const WireTapFrameId& >())   // Copy constructor
    .def_readwrite("id_", &WireTapFrameId::id_)
    .def("id",            &WireTapFrameId::id)
    .def("setId",         &WireTapFrameId::setId)
  ;

  // Expose the WireTapNodeId class
  //
  class_< WireTapNodeId >("WireTapNodeId", init< optional< const char* > >())
    .def(init< const WireTapStr& >())       // Parameter constructor
    .def(init< const WireTapNodeId& >())    // Copy constructor
    .def("id",      &WireTapNodeId::id)
    .def("setId",   &WireTapNodeId::setId)
  ;

  // Expose the WireTapClipFormat class in the WireTapClipFormat 
  // scope (WireTapClipFormat_scope)
  //
  scope* WireTapClipFormat_scope = new scope(
  class_< WireTapClipFormat >("WireTapClipFormat", init<  >())
    .def(init< int, int, int, int, int, float, float, 
               WireTapClipFormat::ScanFormat, const char*,
               optional< const char*, const char* > >())
    .def(init< int, int, int, int, float, float, 
               WireTapClipFormat::ScanFormat, const char*,
               optional< const char*, const char* > >())
    .def(init< const WireTapClipFormat& >())
    .def("width",              &WireTapClipFormat::width)
    .def("height",             &WireTapClipFormat::height)
    .def("setWidth",           &WireTapClipFormat::setWidth)
    .def("setHeight",          &WireTapClipFormat::setHeight)
    .def("bitsPerPixel",       &WireTapClipFormat::bitsPerPixel)
    .def("setBitsPerPixel",    &WireTapClipFormat::setBitsPerPixel)
    .def("numChannels",        &WireTapClipFormat::numChannels)
    .def("setNumChannels",     &WireTapClipFormat::setNumChannels)
    .def("frameBufferSize",    &WireTapClipFormat::frameBufferSize)
    .def("setFrameBufferSize", &WireTapClipFormat::setFrameBufferSize)
    .def("frameRate",          &WireTapClipFormat::frameRate)
    .def("setFrameRate",       &WireTapClipFormat::setFrameRate)
    .def("pixelRatio",         &WireTapClipFormat::pixelRatio)
    .def("setPixelRatio",      &WireTapClipFormat::setPixelRatio)
    .def("scanFormat",         &WireTapClipFormat::scanFormat)
    .def("setScanFormat",      &WireTapClipFormat::setScanFormat)
    .def("strToScanFormat",    &WireTapClipFormat::strToScanFormat)
    .def("scanFormatStr",      &WireTapClipFormat::scanFormatStr)
    .def("formatTag",          &WireTapClipFormat::formatTag)
    .def("setFormatTag",       &WireTapClipFormat::setFormatTag)
    .def("metaDataTag",        &WireTapClipFormat::metaDataTag)
    .def("setMetaDataTag",     &WireTapClipFormat::setMetaDataTag)
    .def("metaData",           &WireTapClipFormat::metaData)
    .def("setMetaData",        &WireTapClipFormat::setMetaData)

    .def("FORMAT_MONO",    &WireTapClipFormat::FORMAT_MONO)
    .def("FORMAT_RGB",     &WireTapClipFormat::FORMAT_RGB)
    .def("FORMAT_HLS",     &WireTapClipFormat::FORMAT_HLS)
    .def("FORMAT_YUV",     &WireTapClipFormat::FORMAT_YUV)
    .def("FORMAT_RGBA",    &WireTapClipFormat::FORMAT_RGBA)
    .def("FORMAT_HLSA",    &WireTapClipFormat::FORMAT_HLSA)
    .def("FORMAT_YUVA",    &WireTapClipFormat::FORMAT_YUVA)
    .def("FORMAT_UYVY",    &WireTapClipFormat::FORMAT_UYVY)
    .def("FORMAT_MONO_LE", &WireTapClipFormat::FORMAT_MONO_LE)
    .def("FORMAT_RGB_LE",  &WireTapClipFormat::FORMAT_RGB_LE)
    .def("FORMAT_HLS_LE",  &WireTapClipFormat::FORMAT_HLS_LE)
    .def("FORMAT_YUV_LE",  &WireTapClipFormat::FORMAT_YUV_LE)
    .def("FORMAT_RGBA_LE", &WireTapClipFormat::FORMAT_RGBA_LE)
    .def("FORMAT_HLSA_LE", &WireTapClipFormat::FORMAT_HLSA_LE)
    .def("FORMAT_YUVA_LE", &WireTapClipFormat::FORMAT_YUVA_LE)
    .def("FORMAT_UYVY_LE", &WireTapClipFormat::FORMAT_UYVY_LE)

    .def("FORMAT_MIXED",                     &WireTapClipFormat::FORMAT_MIXED)
    .def("FORMAT_DL_AUDIO_MIXED",            &WireTapClipFormat::FORMAT_DL_AUDIO_MIXED)
    .def("FORMAT_DL_AUDIO_FLOAT",            &WireTapClipFormat::FORMAT_DL_AUDIO_FLOAT)
    .def("FORMAT_DL_AUDIO_FLOAT_LE",         &WireTapClipFormat::FORMAT_DL_AUDIO_FLOAT_LE)
    .def("FORMAT_DL_AUDIO_INT8",             &WireTapClipFormat::FORMAT_DL_AUDIO_INT8)
    .def("FORMAT_DL_AUDIO_INT8_UNSIGNED",    &WireTapClipFormat::FORMAT_DL_AUDIO_INT8_UNSIGNED)
    .def("FORMAT_DL_AUDIO_INT16",            &WireTapClipFormat::FORMAT_DL_AUDIO_INT16)
    .def("FORMAT_DL_AUDIO_INT16_LE",         &WireTapClipFormat::FORMAT_DL_AUDIO_INT16_LE)
    .def("FORMAT_DL_AUDIO_INT24",            &WireTapClipFormat::FORMAT_DL_AUDIO_INT24)
    .def("FORMAT_DL_AUDIO_INT24_LE",         &WireTapClipFormat::FORMAT_DL_AUDIO_INT24_LE)
    .def("FORMAT_DL_AUDIO_INT24_MSB32_LE",   &WireTapClipFormat::FORMAT_DL_AUDIO_INT24_MSB32_LE)
    .def("FORMAT_DL_AUDIO",          &WireTapClipFormat::FORMAT_DL_AUDIO)
    .def("FORMAT_RGB_FLOAT",   &WireTapClipFormat::FORMAT_RGB_FLOAT)
    .def("FORMAT_RGB_FLOAT_LE",&WireTapClipFormat::FORMAT_RGB_FLOAT_LE)
    .def("FORMAT_RGBA_FLOAT",   &WireTapClipFormat::FORMAT_RGBA_FLOAT)
    .def("FORMAT_RGBA_FLOAT_LE",&WireTapClipFormat::FORMAT_RGBA_FLOAT_LE)
    .def("FORMAT_MONO_FLOAT",   &WireTapClipFormat::FORMAT_MONO_FLOAT)
    .def("FORMAT_MONO_FLOAT_LE",&WireTapClipFormat::FORMAT_MONO_FLOAT_LE)
    .def("SCAN_FORMAT_FIELD_1_ODD_STR",  &WireTapClipFormat::SCAN_FORMAT_FIELD_1_ODD_STR)
    .def("SCAN_FORMAT_FIELD_2_ODD_STR",  &WireTapClipFormat::SCAN_FORMAT_FIELD_2_ODD_STR)
    .def("SCAN_FORMAT_FIELD_1_EVEN_STR", &WireTapClipFormat::SCAN_FORMAT_FIELD_1_EVEN_STR)
    .def("SCAN_FORMAT_FIELD_2_EVEN_STR", &WireTapClipFormat::SCAN_FORMAT_FIELD_2_EVEN_STR)
    .def("SCAN_FORMAT_PROGRESSIVE_STR",  &WireTapClipFormat::SCAN_FORMAT_PROGRESSIVE_STR)
    .def("SCAN_FORMAT_UNKNOWN_STR",      &WireTapClipFormat::SCAN_FORMAT_UNKNOWN_STR)
    .staticmethod("FORMAT_YUVA_LE")
    .staticmethod("FORMAT_HLSA_LE")
    .staticmethod("FORMAT_DL_AUDIO_INT8")
    .staticmethod("FORMAT_DL_AUDIO_INT8_UNSIGNED")
    .staticmethod("FORMAT_DL_AUDIO_INT16")
    .staticmethod("FORMAT_DL_AUDIO_FLOAT_LE")
    .staticmethod("FORMAT_HLS")
    .staticmethod("FORMAT_UYVY_LE")
    .staticmethod("FORMAT_RGB_LE")
    .staticmethod("FORMAT_UYVY")
    .staticmethod("FORMAT_DL_AUDIO_MIXED")
    .staticmethod("FORMAT_DL_AUDIO_INT24_LE")
    .staticmethod("FORMAT_DL_AUDIO_INT24_MSB32_LE")
    .staticmethod("FORMAT_DL_AUDIO")
    .staticmethod("FORMAT_HLS_LE")
    .staticmethod("SCAN_FORMAT_PROGRESSIVE_STR")
    .staticmethod("SCAN_FORMAT_UNKNOWN_STR")
    .staticmethod("FORMAT_YUVA")
    .staticmethod("SCAN_FORMAT_FIELD_1_EVEN_STR")
    .staticmethod("FORMAT_MONO")
    .staticmethod("FORMAT_DL_AUDIO_INT24")
    .staticmethod("strToScanFormat")
    .staticmethod("FORMAT_YUV")
    .staticmethod("FORMAT_MONO_LE")
    .staticmethod("FORMAT_MIXED")
    .staticmethod("FORMAT_HLSA")
    .staticmethod("FORMAT_RGBA_LE")
    .staticmethod("FORMAT_DL_AUDIO_INT16_LE")
    .staticmethod("SCAN_FORMAT_FIELD_2_ODD_STR")
    .staticmethod("SCAN_FORMAT_FIELD_1_ODD_STR")
    .staticmethod("SCAN_FORMAT_FIELD_2_EVEN_STR")
    .staticmethod("FORMAT_RGB")
    .staticmethod("FORMAT_DL_AUDIO_FLOAT")
    .staticmethod("FORMAT_YUV_LE")
    .staticmethod("FORMAT_RGBA")
    .staticmethod("FORMAT_RGB_FLOAT")
    .staticmethod("FORMAT_RGB_FLOAT_LE")
    .staticmethod("FORMAT_RGBA_FLOAT")
    .staticmethod("FORMAT_RGBA_FLOAT_LE")
    .staticmethod("FORMAT_MONO_FLOAT")
    .staticmethod("FORMAT_MONO_FLOAT_LE")
    .staticmethod("scanFormatStr")
  );

  // Expose the WireTapClipFormat::ScanFormat Enum as WireTapOS.ScanFormat
  //
  enum_< WireTapClipFormat::ScanFormat >("ScanFormat")
    .value("SCAN_FORMAT_UNKNOWN",      WireTapClipFormat::SCAN_FORMAT_PROGRESSIVE)
    .value("SCAN_FORMAT_FIELD_1_EVEN", WireTapClipFormat::SCAN_FORMAT_FIELD_1_EVEN)
    .value("SCAN_FORMAT_FIELD_2_EVEN", WireTapClipFormat::SCAN_FORMAT_FIELD_2_EVEN)
    .value("SCAN_FORMAT_FIELD_1_ODD",  WireTapClipFormat::SCAN_FORMAT_FIELD_1_ODD)
    .value("SCAN_FORMAT_FIELD_2_ODD",  WireTapClipFormat::SCAN_FORMAT_FIELD_2_ODD)
    .value("SCAN_FORMAT_PROGRESSIVE",  WireTapClipFormat::SCAN_FORMAT_PROGRESSIVE)
    .value("NUM_SCAN_FORMATS",         WireTapClipFormat::NUM_SCAN_FORMATS)
  ;

  delete WireTapClipFormat_scope;

  // Expose the WireTapAudioFormat class which derives from WireTapClipFormat 
  //
  class_< WireTapAudioFormat, bases< WireTapClipFormat >  >("WireTapAudioFormat", init<  >())
    .def(init< const WireTapAudioFormat& >())
    .def(init< int, int, int, float, const char*, 
               optional< const char*, const char* > >())
    .def("numSamples",       &WireTapAudioFormat::numSamples)
    .def("setNumSamples",    &WireTapAudioFormat::setNumSamples)
    .def("bitsPerSample",    &WireTapAudioFormat::bitsPerSample)
    .def("setBitsPerSample", &WireTapAudioFormat::setBitsPerSample)
    .def("sampleRate",       &WireTapAudioFormat::sampleRate)
    .def("setSampleRate",    &WireTapAudioFormat::setSampleRate)
  ;

  // Expose the WireTapServerId class
  //
  class_< WireTapServerId >("WireTapServerId", init< const WireTapServerId& >())
    .def(init< const char*, const char* >())
    .def(init< optional< const char* > >())
    .def("getId",        &WireTapServerId::getId)
    .def("getIPAddr",    &WireTapServerId::getIPAddr)
    .def("getDB",        &WireTapServerId::getDB)
    .def("isValid",      &WireTapServerId::isValid)
    .def("setId",        &WireTapServerId::setId)
    .def("getIPAddr",    &WireTapServerId::getIPAddr)
    .def("setIPAddr",    &WireTapServerId::setIPAddr)
    .def("getStorageId", &WireTapServerId::getStorageId)
    .def("setStorageId", &WireTapServerId::setStorageId)
    .def("getPort",      &WireTapServerId::getPort)
    .def("setPort",      &WireTapServerId::setPort)
  ;

  // Expose the WireTapMetaData class in the class scope
  //
  scope* WireTapMetaData_scope = new scope(
  class_< WireTapMetaData >("WireTapMetaData", init<  >())
    .def(init< const WireTapMetaData& >())
    .def("STREAM_BLOB", &WireTapMetaData::STREAM_BLOB)
    .def("STREAM_XML",  &WireTapMetaData::STREAM_XML)
    .staticmethod("STREAM_XML")
    .staticmethod("STREAM_BLOB")
  );

  // Expose the public Blob class in the WireTapMetaData scope class as
  // WireTapMetaData.Blob
  //
  class_< WireTapMetaData::Blob >("Blob_base", init< const WireTapMetaData::Blob& >())
    .def(init< const char*, const char*, int, int >())
    .def(init< const char* >())
    .def("getData",    &WireTapMetaData::Blob::getData)
    .def("getFormat",  &WireTapMetaData::Blob::getFormat)
    .def("getVersion", &WireTapMetaData::Blob::getVersion)
    .def("getRawData", &WireTapMetaData::Blob::getRawData)
  ;

  delete WireTapMetaData_scope;

  class_< Blob_Wrapper, bases< WireTapMetaData::Blob > >("Blob", init< const char*, const char*, int, int >())
    .def(init< const char* >())
    .def("getData",    &Blob_Wrapper::getData)
    .def("getFormat",  &Blob_Wrapper::getFormat)
    .def("getVersion", &Blob_Wrapper::getVersionWrapperFunction)
    .def("getRawData", &Blob_Wrapper::getRawData)
  ;

  // Expose the client wiretap Init/Uninit functions
  //
  class_< WireTapClient >("WireTapClient", init<>())
    .def(init<>())
    .def("init",    &WireTapClient::init)
  ;
  def("WireTapClientInit",         (bool (*)())&WireTapClientInit);
  def("WireTapClientUninit",       &WireTapClientUninit);

  def("WireTapFindChild",          &WireTapFindChild);
  def("WireTapResolveDisplayPath", &WireTapResolveDisplayPath);

  // Expose the WireTapInt class. This class is needed because "int" in python
  // is not mutable. So for those methods in WireTap Client API whose original C++
  // signatures require a reference of type int, we use a reference of type
  // WireTapInt instead.
  //
  class_< WireTapInt >("WireTapInt", init< optional< int > >())
    .def("__int__", &WireTapInt::operator int) 	// to Python int conversion 
                                               	//   (overloading conversion operator)
    .def( self > int() )		     	// overloading operator >
    .def( self < int() )        		// overloading operator <
    .def( self == int() ) 			// overloading operator ==
    .def( self == self )			// overloading operator ==
  ; 

  // Expose the WireTapServerHandle class, we have to use a wrapper because: 
  // 1. readFrame(), writeFrame() and readStream() use void* arguments which 
  //    cannot be exposed to python.  So we are using the server wrapper class
  //    to get from python a char* pointer to a void*.
  // 2. getVersion() and getProtocolVersion() expect int& as parameters.
  //    However, Python's int is immutable, which means that passing int&
  //    is not allowed.
  //
  class_< WireTapServerHandle, WireTapServerHandle_Wrapper >("WireTapServerHandle", init< const WireTapServerId& >())
    .def(init< optional< const char* > >())
    .def(init< const WireTapServerHandle& >())
    .def("getRootNode",        &WireTapServerHandle::getRootNode)
    .def("getVendor",          &WireTapServerHandle::getVendor)
    .def("getProduct",         &WireTapServerHandle::getProduct)
    .def("getVersion",         &WireTapServerHandle_Wrapper::getVersionWrapperFunction)
    .def("getInfo",   	       &WireTapServerHandle::getInfo)
    .def("getStorageId",       &WireTapServerHandle::getStorageId)
    .def("getProtocolVersion", &WireTapServerHandle_Wrapper::getProtocolVersionWrapperFunction)
    .def("ping",               &WireTapServerHandle::ping)
    .def("ping",               &WireTapServerHandle_Wrapper::ping)
    .def("translatePath",      &WireTapServerHandle::translatePath)
    .def("translatePaths",     &WireTapServerHandle::translatePaths)
    .def("readFrame",          &WireTapServerHandle_Wrapper::readFrameWrapperFunction)
    .def("writeFrame",         &WireTapServerHandle_Wrapper::writeFrameWrapperFunction)
    .def("getHostName",        &WireTapServerHandle::getHostName)
    .def("getHostUUID",        &WireTapServerHandle::getHostUUID)
    .def("getDisplayName",     &WireTapServerHandle::getDisplayName)
    .def("getId",              &WireTapServerHandle::getId,
                               return_value_policy< copy_const_reference >())
    .def("getIdStr",           &WireTapServerHandle::getIdStr)
    .def("stop",               &WireTapServerHandle::stop)
    .def("lastError",          &WireTapServerHandle::lastError)
    .def("pushStream",         &WireTapServerHandle::pushStream)
    .def("pullStream",         &WireTapServerHandle::pullStream)
    .def("readStream",         &WireTapServerHandle_Wrapper::readStreamWrapperFunction)
    .def("disconnect",         &WireTapServerHandle::disconnect)
    .def("isConnected",        &WireTapServerHandle::isConnected)
  ;

  // Expose the WireTapNodeHandle class, we have to use a wrapper because: 
  // 1. There are 2 overloaded functions "createNode()/createClipNode()".
  // 2. The functions "readFrame()/writeFrame()" are using a void* arguments,
  //    which cannot be exposed to python. So we are using the server wrapper
  //    class to get from python a char* pointer and cast it to a void* pointer.
  // 3. The function "linkToFrames()" is expecting an array of WireTapstr from
  //    python. However, python can only create a 'list' of WireTapStr, because
  //    array in python is reserved only for basic types such as int, char.
  //    Therefore, a wrapper to convert a list of WireTapStr in python to 
  //    an array of WireTapStr is needed.
  // 4. The functions
  //       getNumChildren()/getNumFrames()/getNodeType()/getNumAvailableMetaDataStreams()
  //    expect int& as parameters. However, Python's int is immutable, which means
  //    when calling these funtions within python, passing int& is not allowed. Hence,
  //    wrapper functions are needed so that for these 4 functions, we pass
  //    WireTapInt& as parameters (instead of int&) within Python scripts/programs.
  // 5. The function
  //       getIsClipNode expects bool& so we use the wrapper class and use a WireTapInt
  class_< WireTapNodeHandle, WireTapNodeHandle_Wrapper >("WireTapNodeHandle", init<>())
    .def(init< const WireTapNodeHandle& >())
    .def(init< const WireTapServerHandle&, const WireTapNodeId& >())
    .def(init< const WireTapServerHandle&, const char* >())
    .def("getMetaData", &WireTapNodeHandle::getMetaData,
                        &WireTapNodeHandle_Wrapper::default_getMetaData)
    .def("setMetaData", &WireTapNodeHandle::setMetaData)
    .def("getNodeId",   &WireTapNodeHandle::getNodeId,
                        return_value_policy< reference_existing_object >())
    .def("setNodeId",   &WireTapNodeHandle::setNodeId)
    .def("getNumChildren", &WireTapNodeHandle_Wrapper::getNumChildrenWrapperFunction)
    .def("getChild",       &WireTapNodeHandle::getChild)
    .def("getParentNode",  &WireTapNodeHandle::getParentNode)
    .def("createNode",     (bool (WireTapNodeHandle::*)(const char*, int, WireTapNodeHandle&) )&WireTapNodeHandle::createNode)
    .def("createNode",     (bool (WireTapNodeHandle::*)(const char*, const char*, WireTapNodeHandle&) )&WireTapNodeHandle::createNode)
    .def("createClipNode", (bool (WireTapNodeHandle::*)(const char*, const WireTapClipFormat&, const char*, WireTapNodeHandle&) )&WireTapNodeHandle::createClipNode)
    .def("createClipNode", (bool (WireTapNodeHandle::*)(const char*, const WireTapClipFormat&, int, WireTapNodeHandle&) )&WireTapNodeHandle::createClipNode)
    .def("canCreateNode",  &WireTapNodeHandle::canCreateNode)
    .def("renameNode",     &WireTapNodeHandle::renameNode)
    .def("destroyNode",    &WireTapNodeHandle::destroyNode)
    .def("duplicateNode",  &WireTapNodeHandle::duplicateNode)
    .def("getIsClipNode",  &WireTapNodeHandle_Wrapper::getIsClipNodeWrapperFunction)
    .def("getNodeType",    &WireTapNodeHandle_Wrapper::getNodeTypeWrapperFunction)
    .def("getNodeTypeStr", &WireTapNodeHandle::getNodeTypeStr)
    .def("getDisplayName", &WireTapNodeHandle::getDisplayName)
    .def("getClipFormat",  &WireTapNodeHandle::getClipFormat)
    .def("getNumAvailableMetaDataStreams", &WireTapNodeHandle_Wrapper::getNumAvailableMetaDataStreamsWrapperFunction)
    .def("getAvailableMetaDataStream",     &WireTapNodeHandle::getAvailableMetaDataStream)
    .def("getStreamId",    &WireTapNodeHandle::getStreamId)
    .def("readFrame",      (bool (WireTapNodeHandle_Wrapper::*)(int, char *, int, char*, int)) &WireTapNodeHandle_Wrapper::readFrameWrapperFunction)
    .def("readFrame",      (bool (WireTapNodeHandle_Wrapper::*)(int, char *, int)) &WireTapNodeHandle_Wrapper::readFrameWrapperFunction)
    .def("writeFrame",     &WireTapNodeHandle_Wrapper::writeFrameWrapperFunction)
    .def("getFrameId",     &WireTapNodeHandle::getFrameId)
    .def("getFrameIdPath", &WireTapNodeHandle::getFrameIdPath)
    .def("setNumFrames",   &WireTapNodeHandle::setNumFrames)
    .def("getNumFrames",   &WireTapNodeHandle_Wrapper::getNumFramesWrapperFunction)
    .def("linkToFrames",   &WireTapNodeHandle_Wrapper::linkToFramesWrapperFunction)
    .def("lastError",      &WireTapNodeHandle::lastError)
    .def("getServer",      &WireTapNodeHandle::getServer, return_value_policy< copy_const_reference >())
    .def("setServer",      &WireTapNodeHandle::setServer)
  ;

  // Expose the WireTapServerList class in the WireTapServerList scope class
  //
  scope* WireTapServerList_scope = new scope(
  class_< WireTapServerList >("WireTapServerList_Base", init<  >())
    .def(init< const WireTapServerList& >())
    .def("resolve",          &WireTapServerList::resolve)
    .def("resolveStorageId", &WireTapServerList::resolveStorageId)
    .def("getNumNodes",	     &WireTapServerList::getNumNodes)
    .def("getNode",          &WireTapServerList::getNode)
    .def("lastError",        &WireTapServerList::lastError)
  );

  delete WireTapServerList_scope;

  //  Expose the WireTapServerList_Wrapper struct
  //
  class_< WireTapServerList_Wrapper, bases< WireTapServerList > >("WireTapServerList", init<>())
    .def(init< const char*, const char* >())
    .def("resolve",          &WireTapServerList_Wrapper::resolve)
    .def("resolveStorageId", &WireTapServerList_Wrapper::resolveStorageId)
    .def("getNumNodes",      &WireTapServerList_Wrapper::getNumNodesWrapperFunction)
    .def("getNode",          &WireTapServerList_Wrapper::getNode)
    .def("lastError",        &WireTapServerList_Wrapper::lastError)
  ;
}
