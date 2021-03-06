function ds = pascal_test(model, M)
% Compute bounding boxes in a test set.
%   ds = pascal_test(model, testset, year, suffix)
%
% Return value
%   ds      Detection clipped to the image boundary. Cells are index by image
%           in the order of the PASCAL ImageSet file for the testset.
%           Each cell contains a matrix who's rows are detections. Each
%           detection specifies a clipped subpixel bounding box and its score.
% Arguments
%   model   Model to test
%   testset Dataset to test the model on (e.g., 'val', 'test')
%   year    Dataset year to test the model on  (e.g., '2007', '2011')
%   suffix  Results are saved to a file named:
%           [model.class '_boxes_' testset '_' suffix]
%
%   We also save the bounding boxes of each filter (include root filters)
%   and the unclipped detection window in ds

% AUTORIGHTS
% -------------------------------------------------------
% Copyright (C) 2011-2012 Ross Girshick
% Copyright (C) 2008, 2009, 2010 Pedro Felzenszwalb, Ross Girshick
% 
% This file is part of the voc-releaseX code
% (http://people.cs.uchicago.edu/~rbg/latent/)
% and is available under the terms of an MIT-like license
% provided in COPYING. Please retain this notice and
% COPYING if you use this file (or a portion of it) in
% your project.
% -------------------------------------------------------

conf = voc_config();
cachedir = conf.paths.model_dir;
cls = model.class;


% run detector in each image
try
  load([cachedir cls '_boxes']);
catch
  % parfor gets confused if we use VOCopts
  num_ids = size(M,1);
  if size(M,2)>96*96+5 % hack for testset/CV set
      st1=31;
  else
      st1=2;
  end      
  ds_out = cell(1, num_ids);
  bs_out = cell(1, num_ids);
  th = tic();
  for i = 1:num_ids;
    fprintf('%s: testing: %d/%d\n', cls, ...
            i, num_ids);
    m=M(i,st1:end);
    im=reshape(m,96,[])'; 
    [ds, bs] = imgdetect(im, model, model.thresh);
    if ~isempty(bs)
      unclipped_ds = ds(:,1:4);
      [ds, bs, rm] = clipboxes(im, ds, bs);
      unclipped_ds(rm,:) = [];

      % NMS
      I = nms(ds, 0.1);                 % different overlap than default, because all the elements we want are non overlapping
      ds = ds(I,:);
      bs = bs(I,:);
      unclipped_ds = unclipped_ds(I,:);

      % Save detection windows in boxes
      ds_out{i} = ds(:,[1:4 end]);

      % Save filter boxes in parts
      if model.type == model_types.MixStar
        % Use the structure of a mixture of star models 
        % (with a fixed number of parts) to reduce the 
        % size of the bounding box matrix
        bs = reduceboxes(model, bs);
        bs_out{i} = bs;
      else
        % We cannot apply reduceboxes to a general grammar model
        % Record unclipped detection window and all filter boxes
        bs_out{i} = cat(2, unclipped_ds, bs);
      end
    else
      ds_out{i} = [];
      bs_out{i} = [];
    end
  end
  th = toc(th);
  ds = ds_out;
  bs = bs_out;
  save([cachedir cls '_boxes'], ...
       'ds', 'bs', 'th');
  fprintf('Testing took %.4f seconds\n', th);
end
