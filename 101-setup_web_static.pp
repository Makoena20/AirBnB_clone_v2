# 101-setup_web_static.pp

# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Ensure Nginx service is running and enabled
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => Package['nginx'],
}

# Define web_static directory
file { '/data':
  ensure => 'directory',
}

# Define web_static/releases and web_static/shared directories
file { ['/data/web_static/releases', '/data/web_static/shared']:
  ensure => 'directory',
}

# Create a symbolic link from current to releases/test
file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test',
  require => File['/data/web_static/releases'],
}

# Create index.html file inside releases/test directory
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '<html>\n<head>\n</head>\n<body>\n  Holberton School\n</body>\n</html>\n',
  require => File['/data/web_static/releases/test'],
}

# Restart Nginx if any file in the /data directory changes
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => File['/data'],
}


