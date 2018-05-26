# The File System encoding described in Forensics Day Off
#
# The encoding defines a format for storing numbered files on binary Random
# Access Storage. The storage is broken into octets, and blocks of 8 octets
# each.
#
# The header describes the positions and lengths of the files. The header
# consists of the first four blocks on the disk. The octets therein are taken
# in pairs to describe files. There are 16 such pairs, one for each possible
# file.
# 
# The first octet of a header pair stores the offset of its file in blocks,
# starting from the start of the disk. An offset of 3 or less indicates the
# file is unallocated.
#
# The second octet of a header pair stores the length of a file in octets.
#
# The rest of the disk stores the file data.

from cryptoamino import tools

class FileSystem:
  
  def __init__(self):
    self.header_blocks = 4
    self.block_size = 8
  
  # 'files' must be an iterable of byte arrays (files), or Nones for
  # unallocated files.
  # Only the first 255 octets each of the files will be stored.
  # As many files can be stored as there can be described in the header size.
  def encode(self, files):
    
    # The first 255 octets each of the stored files.
    max_files = self.header_blocks*self.block_size//2
    truncated_files = [
      None if f is None else f[0:255]
      for f in files[0:max_files]]
    
    # Files padded to block boundaries.
    file_lengths = []
    padded_files = []
    for f in truncated_files:
      if f is None: # Skip unallocated files
        file_lengths.append(0)
        padded_files.append(None)
      else:
        file_length = len(f)
        octets_left = -file_length % self.block_size
        padded_file = f + bytearray(octets_left)
        file_lengths.append(file_length);
        padded_files.append(padded_file)
    
    # File arrangement
    file_offsets = []
    next_available_offset = self.header_blocks
    for f in padded_files:
      if f is None:
        file_offsets.append(0)
      else:
        file_offsets.append(next_available_offset)
        file_blocks = len(f) // self.block_size
        next_available_offset += file_blocks
    
    # File System header
    header = bytearray(self.block_size * self.header_blocks)
    for i in range(0, len(truncated_files)):
      file_offset = file_offsets[i]
      file_length = file_lengths[i]
      header[i*2] = file_offset
      header[i*2 + 1] = file_length
    
    # Construct image
    image = header
    for f in padded_files:
      if f is not None:
        image += f
    
    return image
  
  # 'image' must be a byte array, and valid disk image.
  # Yields byte arrays for allocated files, and Nones for unallocated files.
  def decode(self, image):
    
    # Extract the header
    header = image[0 : self.block_size*self.header_blocks]
    
    # Extract the file details
    metadata = tools.group(header, 2)
    for file_offset, file_length in metadata:
      if file_offset < self.header_blocks:
        yield None
      else:
        start_octet = file_offset*self.block_size
        file_content = image[start_octet : start_octet+file_length]
        yield file_content
