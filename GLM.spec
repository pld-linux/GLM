#
# Conditional build:
%bcond_without	tests		# build without tests
#
Summary:	OpenGL Mathematics (GLM)
Name:		GLM
Version:	0.9.4.4
Release:	1
License:	MIT
Group:		Applications
Source0:	http://downloads.sourceforge.net/ogl-math/glm-%{version}.7z
# Source0-md5:	1c5a626c025dff9664b08d8f39c7e11b
URL:		http://glm.g-truc.net/
BuildRequires:	cmake
BuildRequires:	p7zip-standalone
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenGL Mathematics (GLM) is a C++ mathematics library for graphics
software based on the OpenGL Shading Language (GLSL) specification.

GLM is a header only library, there is nothing to build,
just include it.

%prep
%setup -q -n glm-%{version}

%build
mkdir build
cd build
%cmake \
	../ \
	-DGLM_TEST_ENABLE:BOOL=%{!?with_tests:OFF}%{?with_tests:ON}

%{?with_tests:%{__make}}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

cd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc readme.txt doc/glm.pdf
%attr(755,root,root) %{_includedir}/glm
