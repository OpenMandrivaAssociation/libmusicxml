%define _enable_debug_packages %{nil}
%define debug_package %{nil}

Summary:	A dummy package for bs testing purpose
Name:		null
Version:	2.2
Release:	1.10
Epoch:		1
Group:		Development/Other
License:	GPL

%description
Dummy package.

%package dummy
Group:		Development/Other
Summary:	Test package

%description dummy
A dummy subpackage.

%prep
%setup -D -T -n .

%build

%install
mkdir -p %{buildroot}

%post -p /bin/csh
echo "csh sux"

%files
%files dummy

