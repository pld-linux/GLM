#
# Conditional build:
%bcond_without	tests		# build without tests
%bcond_with	p7zip		# plain p7zip (compatible with both rpm4/rpm5)
#
%define		gitref	47585fde0c49fa77a2bf2fb1d2ead06999fd4b6e
%define		snap	20230818
%define		rel	1

Summary:	OpenGL Mathematics (GLM) - C++ mathematics library for GLSL
Summary(pl.UTF-8):	OpenGL Mathematics (GLM) - biblioteka matematyczna C++ dla GLSL
Name:		GLM
Version:	0.9.9.9
Release:	0.%{snap}.%{rel}
License:	MIT
Group:		Development/Libraries
#Source0Download: https://github.com/g-truc/glm/releases
Source0:	https://github.com/g-truc/glm/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	b288cb704cca5d1cd46be724ce61f428
Patch0:		x32.patch
URL:		https://glm.g-truc.net/
BuildRequires:	cmake >= 3.2
%{?with_tests:BuildRequires:	libstdc++-devel}
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with p7zip}
BuildRequires:	p7zip
%else
BuildRequires:	p7zip-standalone
BuildRequires:	rpm-build >= 5
%endif
Requires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages	0

%description
OpenGL Mathematics (GLM) is a C++ mathematics library for graphics
software based on the OpenGL Shading Language (GLSL) specification.

GLM is a header only library, there is nothing to build, just include
it.

%description -l pl.UTF-8
OpenGL Mathematics (GLM) to biblioteka matematyczna C++ dla programów
graficznych opartych na specyfikacji OpenGL Shading Language (GLSL).

%prep
%if %{with p7zip}
%setup -q -c -T -n glm
7z x %{SOURCE0} -o..
%else
%setup -q -n glm-%{gitref}
%endif
%patch0 -p1

%build
mkdir build
cd build
CXXFLAGS="%{rpmcxxflags} -fno-ipa-modref" \
%cmake .. \
	-DGLM_TEST_ENABLE:BOOL=%{!?with_tests:OFF}%{?with_tests:ON}

%if %{with tests}
%{__make}
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc manual.md readme.md
%{_includedir}/glm
%{_libdir}/cmake/glm
