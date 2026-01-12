#
# Conditional build:
%bcond_without	tests	# test suite
#
Summary:	OpenGL Mathematics (GLM) - C++ mathematics library for GLSL
Summary(pl.UTF-8):	OpenGL Mathematics (GLM) - biblioteka matematyczna C++ dla GLSL
Name:		GLM
Version:	1.0.2
Release:	2
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/g-truc/glm/releases
Source0:	https://github.com/g-truc/glm/archive/%{version}/glm-%{version}.tar.gz
# Source0-md5:	1215b4d29f7a34933f941411bda228a2
Patch0:		x32.patch
URL:		https://glm.g-truc.net/
BuildRequires:	cmake >= 3.6
%{?with_tests:BuildRequires:	libstdc++-devel}
BuildRequires:	rpmbuild(macros) >= 2.047
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenGL Mathematics (GLM) is a C++ mathematics library for graphics
software based on the OpenGL Shading Language (GLSL) specification.

%description -l pl.UTF-8
OpenGL Mathematics (GLM) to biblioteka matematyczna C++ dla programów
graficznych opartych na specyfikacji OpenGL Shading Language (GLSL).

%package devel
Summary:	OpenGL Mathematics (GLM) - C++ mathematics library for GLSL (header files)
Summary(pl.UTF-8):	OpenGL Mathematics (GLM) - biblioteka matematyczna C++ dla GLSL (pliki nagłówkowe)
Group:		Development/Libraries
Requires:	libstdc++-devel
# no base dependency - can be used as header-only library
# not noarch due to paths in cmake configs
Obsoletes:	GLM < 1.0.1

%description devel
OpenGL Mathematics (GLM) is a C++ mathematics library for graphics
software based on the OpenGL Shading Language (GLSL) specification.

%description devel -l pl.UTF-8
OpenGL Mathematics (GLM) to biblioteka matematyczna C++ dla programów
graficznych opartych na specyfikacji OpenGL Shading Language (GLSL).

%prep
%setup -q -n glm-%{version}
%patch -P0 -p1

%build
install -d build
cd build
# change CMAKE_INSTALL_DATAROOTDIR to arch-dependent (files contain arch-dependent libglm.so paths)
%cmake .. \
	-DCMAKE_INSTALL_DATAROOTDIR=%{_libdir}/cmake \
	-DGLM_BUILD_TESTS:BOOL=%{__ON_OFF tests}

%{__make}

%if %{with tests}
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc manual.md readme.md
%{_libdir}/libglm.so

%files devel
%defattr(644,root,root,755)
%doc manual.md readme.md
%{_includedir}/glm
%{_libdir}/cmake/glm
