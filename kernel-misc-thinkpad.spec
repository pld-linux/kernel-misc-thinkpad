#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)

%define		_name thinkpad
%define 	_rel 1
Summary:	Linux drivers for ThinkPad laptops
Summary(pl):	Sterowniki dla Linuksa do laptopów ThinkPad
Name:		kernel%{_alt_kernel}-misc-thinkpad
Version:	6.0
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/tpctl/%{_name}_%{version}.tar.gz
# Source0-md5:	d6549f4fe51f594a20d1498f06def010
URL:		http://tpctl.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.308
%if %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Requires(post,postun):	/sbin/depmod
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
These are drivers for ThinkPad laptops for Linux.

This package contains Linux modules.

%description -l pl
Sterowniki dla Linuksa do laptopów ThinkPad.

Ten pakiet zawiera modu³y j±dra Linuksa.

%package -n kernel%{_alt_kernel}-smp-misc-thinkpad
Summary:	Linux SMP drivers for ThinkPad laptops
Summary(pl):	Sterowniki dla Linuksa SMP do laptotów ThinkPad
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Requires(post,postun):	/sbin/depmod

%description -n kernel%{_alt_kernel}-smp-misc-thinkpad
These are drivers for ThinkPad laptops for Linux.

This package contains Linux SMP modules.

%description -n kernel%{_alt_kernel}-smp-misc-thinkpad -l pl
Sterowniki dla Linuksa do laptopów ThinkPad.

Ten pakiet zawiera modu³y j±dra Linuksa SMP.

%prep
%setup -q -n %{_name}-%{version}

%build
_PWD=`pwd`
cd 2.6/drivers
# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} o/include/asm
%if %{with dist_kernel}
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif
#
#	patching/creating makefile(s) (optional)
#
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o -name '*.s' -o" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		EXTRA_CFLAGS="-I$PWD/../include -DLINUX" \
		CC="%{__cc}" CPP="%{__cpp}" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}

	mv thinkpad{,-$cfg}.ko
	mv smapi{,-$cfg}.ko
	mv superio{,-$cfg}.ko
	mv rtcmosram{,-$cfg}.ko
done
cd $_PWD

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man4
install man/thinkpad.4 $RPM_BUILD_ROOT%{_mandir}/man4

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc/thinkpad
install 2.6/drivers/thinkpad-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/thinkpad/thinkpad.ko
install 2.6/drivers/smapi-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/thinkpad/smapi.ko
install 2.6/drivers/superio-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/thinkpad/superio.ko
install 2.6/drivers/rtcmosram-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/thinkpad/rtcmosram.ko
%if %{with smp} && %{with dist_kernel}
install 2.6/driver/thinkpad-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/thinkpad/thinkpad.ko
install 2.6/driver/smapi-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/thinkpad/smapi.ko
install 2.6/driver/superio-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/thinkpad/superio.ko
install 2.6/driver/rtcmosram-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/thinkpad/rtcmosram.ko
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-misc-thinkpad
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-misc-thinkpad
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README SUPPORTED-MODELS TECHNOTES
/lib/modules/%{_kernel_ver}/misc/thinkpad
%{_mandir}/man4/thinkpad.4*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-misc-thinkpad
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README SUPPORTED-MODELS TECHNOTES
/lib/modules/%{_kernel_ver}smp/misc/thinkpad
# i know it would get double packed when up & smp installed, but rpm handles this
%{_mandir}/man4/thinkpad.4*
%endif
